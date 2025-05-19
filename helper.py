import subprocess
import os

def get_prompt_context(image_filename: str) -> str:
    """
    Adds context prompt based on filename prefix.
    """
    name = image_filename.lower()
    if name.startswith("drawing_"):
        return "This is a hand-drawn illustration. Describe the scene, actions, and objects in detail."
    elif name.startswith("text_"):
        return "This is a scanned text document. Read and summarize the visible text accurately."
    elif name.startswith("flowchart_"):
        return "This is a diagram or flowchart. Describe the process, arrows, and structure clearly."
    else:
        return ""

def ask_llava(image_path: str, question: str, timeout: int = 30) -> str:
    """
    Calls ollama run llava:7b with the image and question as prompt.
    """
    filename = os.path.basename(image_path)
    context = get_prompt_context(filename)
    full_prompt = f"![image]({image_path})\n{context}\n{question.strip()}\n"

    try:
        process = subprocess.Popen(
            ["ollama", "run", "llava:7b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, _ = process.communicate(input=full_prompt.encode("utf-8"), timeout=timeout)
        response = stdout.decode("utf-8", errors="replace").strip()
        return response.replace('\n\n', '\n')[:400]

    except subprocess.TimeoutExpired:
        process.kill()
        return "Error: Timeout"
    except Exception as e:
        return f"Error: {str(e)}"
