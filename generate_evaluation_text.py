import json
import os

ALL_ANSWERS_FILE = "all_answers.txt"
GROUND_TRUTH_FILE = "gt.txt" # Corrected path to root directory
OUTPUT_TEXT_FILE = "evaluation_input_for_chatgpt.txt"

def load_answers(filepath):
    """Loads answers from a JSON lines file."""
    answers = {}
    if not os.path.exists(filepath):
        print(f"Warning: File not found at {filepath}")
        return answers
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            try:
                data = json.loads(line.strip())
                # Create a unique key for matching
                # Normalize to lower case and strip whitespace for more robust matching
                picture_key = data.get("picture", "").strip().lower()
                question_key = data.get("question", "").strip().lower()
                
                if not picture_key or not question_key:
                    print(f"Warning: Missing picture or question in {filepath} at line {line_num + 1}. Skipping.")
                    continue
                
                key = (picture_key, question_key)
                if key in answers:
                    print(f"Warning: Duplicate key {key} found in {filepath}. Overwriting previous entry.")
                answers[key] = data.get("answer", "").strip()
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from line {line_num + 1} in {filepath}. Skipping.")
            except AttributeError as e:
                print(f"Warning: Problem accessing data in {filepath} at line {line_num + 1}: {e}. Skipping. Line content: {line.strip()}")
    return answers

def main():
    model_answers_data = load_answers(ALL_ANSWERS_FILE)
    ground_truth_data = load_answers(GROUND_TRUTH_FILE)

    if not model_answers_data:
        print(f"No data loaded from {ALL_ANSWERS_FILE}. Cannot generate evaluation text.")
        return
    if not ground_truth_data:
        print(f"No data loaded from {GROUND_TRUTH_FILE}. Evaluation text will only contain model answers.")

    output_lines = []
    instructions = [
        "Please evaluate the model's answers based on the following criteria and calculate the accuracy score.",
        "For each question-answer pair:",
        "- If the Model Answer is Correct compared to the Ground Truth Answer, award 1 point.",
        "- If the Model Answer is Partially Correct, award 0.5 points.",
        "- If the Model Answer is Incorrect or irrelevant, award 0 points.",
        "",
        "After evaluating all pairs, calculate the 'Answer Score' as:",
        "Answer Score = (Total points awarded) / (Total number of questions evaluated)",
        "",
        "The final grade also includes a UI score, but for this text, focus on the Answer Score.",
        "--- (Start of Evaluation Data) ---",
        ""
    ]
    output_lines.extend(instructions)
    
    matched_pairs = 0
    unmatched_model_answers = 0
    questions_for_evaluation_count = 0


    for (picture, question_text_key), model_answer in model_answers_data.items():
        # Attempt to find the original question text for display (non-lowercased)
        # This requires re-reading all_answers.txt or storing original questions,
        # for simplicity, we'll use the key version for now or assume user can map it.
        # A more robust solution would store original question text alongside the key.
        
        # For display, we need the original casing of picture and question if possible.
        # This simple version will use the keys which are lowercased.
        # To get original casing, one would need to iterate through original files again
        # or store more info in the load_answers function.
        # For now, we'll use the processed keys for picture and question display.
        
        # Find original question text (this is a bit inefficient but ensures original casing for output)
        original_question_display = question_text_key
        original_picture_display = picture
        
        # This part is tricky without storing original data. Let's assume we need to find it.
        # For now, I'll just use the key for display.
        # A better way: store the full original record in load_answers if original casing is critical for the prompt.

        gt_answer = ground_truth_data.get((picture, question_text_key))

        output_lines.append(f"Image: {picture}") # Using the key 'picture' which is lowercased
        output_lines.append(f"Question: {question_text_key}") # Using the key 'question_text_key' which is lowercased
        output_lines.append(f"Model Answer: {model_answer}")

        if gt_answer is not None:
            output_lines.append(f"Ground Truth Answer: {gt_answer}")
            matched_pairs += 1
            questions_for_evaluation_count +=1 # Only count if GT is available for fair scoring
        else:
            output_lines.append("Ground Truth Answer: [Not Found - This pair will not be part of the score calculation]")
            # unmatched_model_answers +=1 # This is already captured by len(model_answers_data) - matched_pairs if we only care about pairs with GT
        
        output_lines.append("---") # Separator

    if not model_answers_data: # Check if there were any model answers to begin with
        print("No model answers found in all_answers.txt to generate text.")
        return

    with open(OUTPUT_TEXT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))
    
    print(f"Evaluation text generated and saved to {OUTPUT_TEXT_FILE}")
    print(f"Total model answer entries processed from {ALL_ANSWERS_FILE}: {len(model_answers_data)}")
    print(f"Total ground truth entries processed from {GROUND_TRUTH_FILE}: {len(ground_truth_data)}")
    print(f"Number of question-answer pairs matched with ground truth (for scoring): {questions_for_evaluation_count}")
    
    unmatched_model_count = len(model_answers_data) - matched_pairs
    if unmatched_model_count > 0:
        print(f"Number of model answers for which no ground truth was found: {unmatched_model_count}")
    
    unmatched_gt_count = len(ground_truth_data) - matched_pairs
    if unmatched_gt_count > 0:
        print(f"Number of ground truth answers not matched by any model answer: {unmatched_gt_count}")

if __name__ == "__main__":
    main()