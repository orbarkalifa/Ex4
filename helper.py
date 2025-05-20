import subprocess
import os
import json

def get_prompt_context(image_filename: str) -> str:
    name = image_filename.lower()
    if name.startswith("drawing_"):
        return (
            "This is a hand-drawn illustration. "
            "Do not assume anything beyond what is clearly shown. "
            "Focus only on visible objects, actions, and scene layout."
        )
    elif name.startswith("text_"):
        return (
            "This is a scanned text page. "
            "Only use visible, legible text. "
            "Do not guess missing words. If unreadable, say so."
        )
    elif name.startswith("flowchart_"):
        return (
            "This is a flowchart or diagram. "
            "Only describe what is visually connected in the layout. "
            "Focus on arrows, steps, and visible labels. "
            "Do not speculate on function or meaning beyond the diagram."
        )
    return (
        "Only describe what is clearly shown in the image. "
        "Do not assume or add context."
    )

def ask_llava(image_path: str, question: str, timeout: int = 30) -> str:
    filename = os.path.basename(image_path)
    context = get_prompt_context(filename)
    prompt = f"![image]({image_path})\n{context}\n{question.strip()}\n"

    try:
        process = subprocess.Popen(
            ["ollama", "run", "llava:7b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, _ = process.communicate(input=prompt.encode("utf-8"), timeout=timeout)
        response = stdout.decode("utf-8", errors="replace").strip()
        return response.replace('\n\n', '\n')[:400]
    except subprocess.TimeoutExpired:
        process.kill()
        return "Error: Timeout"
    except Exception as e:
        return f"Error: {str(e)}"

def save_response(image_path: str, question: str, answer: str):
    out_path = os.path.abspath("all_answers.txt")
    record = {
        "picture": os.path.basename(image_path),
        "question": question.strip(),
        "answer": answer.strip()
    }
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def run_batch_on_folder(folder_path: str):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    out_path = os.path.join(folder_path, "all_answers.txt")

    if os.path.exists(out_path):
        os.remove(out_path)

    for image_file in image_files:
        image_path = os.path.abspath(os.path.join(folder_path, image_file))
        name = os.path.splitext(image_file)[0]
        question_file = os.path.join(folder_path, f"{name}.txt")

        if not os.path.exists(question_file):
            continue

        with open(question_file, "r", encoding="utf-8") as f:
            questions = f.readlines()

        for question in questions:
            question = question.strip()
            if not question:
                continue
            answer = ask_llava(image_path, question)
            save_response(image_path, question, answer)
