import subprocess
import os
import json


def get_image_specific_guidance(image_filename: str) -> str:
    name = os.path.basename(image_filename).lower()
    if name.startswith("drawing_"):
        return ("For this drawing: Look carefully at all depicted elements. "
                "If the question asks for a count, provide it. If it asks about an action or state (e.g., open/closed, color), describe that specific observation based *only* on what you see.")
    elif name.startswith("text_"):
        return (
            "This image contains text. Your main task is to **read the text carefully and accurately** to find the answer. "
            "If text is small or slightly unclear, try your best to decipher it. Re-read relevant parts if needed.")
    elif name.startswith("flowchart_"):
        return (
            "This image is a flowchart. **Trace the connections (lines and arrows) meticulously. Read all text in every box and on every connector.** "
            "Use this to answer questions about the process or structure shown.")
    return "Carefully examine all visual details in the image to locate the information needed to answer the question."


def ask_llava(image_path: str, question: str, timeout: int = 240) -> str:
    absolute_image_path = os.path.abspath(image_path)
    if not os.path.exists(absolute_image_path):
        return "Error: Image file not found: " + absolute_image_path

    filename = os.path.basename(absolute_image_path)
    image_guidance = get_image_specific_guidance(filename)

    # "Direct & Re-examine" Prompt
    prompt_text = f"""![image]({absolute_image_path})

**Task:** Answer the question below.

**Rules:**
1.  Base your answer **strictly and solely** on the visual information in the image above.
2.  **Do not guess, assume, or add any information not explicitly depicted.**
3.  {image_guidance}
4.  **Before concluding information is missing, please take a second look and re-examine the image carefully.** If, after this careful re-examination, the specific information is genuinely not visible or is completely unreadable, your entire response must be *only* the exact phrase: "Information not visible in image."

**Question:**
{question.strip()}

**Answer (from image only):**
"""

    try:
        process = subprocess.Popen(
            ["ollama", "run", "llava:7b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout_data, stderr_data = process.communicate(input=prompt_text, timeout=timeout)

        if process.returncode != 0:
            error_message = f"Error: Ollama process exited with code {process.returncode}. Stderr: {stderr_data.strip()}"
            return error_message[:400]

        response = stdout_data.strip()

        uncertainty_message_exact = "Information not visible in image."

        # If the response is *exactly* the uncertainty message, return it as is.
        if response == uncertainty_message_exact:
            return uncertainty_message_exact

        common_prefixes = [
            "Answer (from image only):",  # From our prompt
            "Answer:",
            "ANSWER:",
        ]
        response_lower = response.lower()
        for prefix in common_prefixes:
            if response_lower.startswith(prefix.lower()):
                response = response[len(prefix):].strip()
                response_lower = response.lower()
                break

        # If, after stripping prefixes, the response is exactly the uncertainty message, return it.
        if response == uncertainty_message_exact:
            return uncertainty_message_exact

        return response.replace('\n\n', '\n')[:400]
    except subprocess.TimeoutExpired:
        process.kill()
        return "Error: LLaVA query timed out after " + str(timeout) + " seconds."
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"[:400]


def save_response(output_file_path: str, image_filename: str, question: str, answer: str):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    escaped_image_filename = os.path.basename(image_filename).replace('"', '\\"')
    escaped_question = question.strip().replace('"', '\\"')
    escaped_answer = answer.strip().replace('"', '\\"')
    entry = (
        f'picture: "{escaped_image_filename}"\n'
        f'question: "{escaped_question}"\n'
        f'answer: "{escaped_answer}"\n\n'
    )
    try:
        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"Error saving response to {output_file_path}: {e}")


def run_batch_on_folder(folder_path: str):
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at {folder_path}");
        return
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
    output_file_path = os.path.join(folder_path, "all_answers.txt")
    if os.path.exists(output_file_path):
        try:
            os.remove(output_file_path)
        except OSError as e:
            print(f"Warning: Could not remove {output_file_path}. Error: {e}.")
    for image_file in image_files:
        image_full_path = os.path.join(folder_path, image_file)
        base_name = os.path.splitext(image_file)[0]
        question_file_path = os.path.join(folder_path, f"{base_name}.txt")
        if not os.path.exists(question_file_path):
            print(f"Info: Skipping {image_file} - no matching .txt file.");
            continue
        try:
            with open(question_file_path, "r", encoding="utf-8") as f:
                questions = f.readlines()
        except Exception as e:
            print(f"Error reading {question_file_path}: {e}"); continue
        print(f"\nProcessing image: {image_file}")
        for question_text in questions:
            question_text = question_text.strip()
            if not question_text: continue
            print(f"  Asking: {question_text[:70]}...")
            answer_text = ask_llava(image_full_path, question_text)
            save_response(output_file_path, image_file, question_text, answer_text)
            print(f"    -> Answer (first 70 chars): {answer_text[:70].replace(os.linesep, ' ')}")
    print(f"\nBatch processing complete for {folder_path}. Output: {output_file_path}")