import os
import json
from helper import ask_llava

IMG_DIR = "images"
Q_DIR = "questions"
OUTPUT_FILE = "all_answers.txt"

results = []

for filename in os.listdir(IMG_DIR):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    name = os.path.splitext(filename)[0]
    image_path = os.path.abspath(os.path.join(IMG_DIR, filename))
    question_path = os.path.join(Q_DIR, f"{name}.txt")

    if not os.path.exists(question_path):
        print(f"[!] Skipping {filename} — missing matching .txt file")
        continue

    with open(question_path, "r", encoding="utf-8") as qf:
        questions = qf.readlines()

    for question in questions:
        question = question.strip()
        if not question:
            continue

        answer = ask_llava(image_path, question)
        result = {
            "picture": filename,
            "question": question,
            "answer": answer
        }
        results.append(result)
        print(f"[✓] {filename}: {question[:40]}...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"✅ Done! {len(results)} answers written to {OUTPUT_FILE}")
