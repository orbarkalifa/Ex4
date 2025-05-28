import streamlit as st
import os
from helper import ask_llava, save_response, run_batch_on_folder  # No caches imported from helper

st.set_page_config(page_title="LLaVA Image Analyzer", layout="centered")

st.markdown("# 🧠 LLaVA:7b – Visual Question Answering (Direct Single-Pass)")
st.markdown("Uses a strong, direct single-pass prompt for each question.")
st.divider()

UPLOAD_OUTPUT_DIR = "temp_uploads"
os.makedirs(UPLOAD_OUTPUT_DIR, exist_ok=True)

# No session state related to helper caches needed here anymore.

tab1, tab2, tab3 = st.tabs(["📂 Folder Mode (Single Image)", "📦 Batch Mode (Whole Folder)", "📥 Upload Image"])

# ======================= TAB 1: FOLDER MODE (SINGLE IMAGE) =======================
with tab1:
    st.subheader("📂 Folder-Based Image + Question")
    st.markdown("""
    **Instructions:**
    1.  Enter folder path with images and `.txt` question files.
    2.  Select an image.
    3.  Select a question.
    4.  Click "▶️ Run" to get the answer using a direct prompt.
    -   Answer saved/appended to `all_answers.txt` **in the selected folder**.
    """)

    if 'folder_path_tab1' not in st.session_state:
        st.session_state.folder_path_tab1 = os.getcwd()
    folder_path_tab1 = st.text_input("Enter folder path:", value=st.session_state.folder_path_tab1,
                                     key="fp_tab1_input_dsp")  # dsp for direct single pass
    st.session_state.folder_path_tab1 = folder_path_tab1

    if os.path.isdir(folder_path_tab1):
        try:
            image_files = sorted(
                [f for f in os.listdir(folder_path_tab1) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
        except Exception as e:
            st.error(f"Error listing files: {e}")
            image_files = []

        if image_files:
            selected_image_filename = st.selectbox("🖼️ Select image", image_files, key="img_select_tab1_dsp")
            if selected_image_filename:
                selected_image_path = os.path.join(folder_path_tab1, selected_image_filename)
                st.image(selected_image_path, caption=selected_image_filename, width=300)

                base_name = os.path.splitext(selected_image_filename)[0]
                question_file_path = os.path.join(folder_path_tab1, f"{base_name}.txt")

                if os.path.exists(question_file_path):
                    try:
                        with open(question_file_path, "r", encoding="utf-8") as f:
                            questions = [line.strip() for line in f if line.strip()]
                    except Exception as e:
                        st.error(f"Error reading question file: {e}")
                        questions = []

                    if questions:
                        selected_question = st.selectbox("📋 Select a question", questions, key="q_select_tab1_dsp")
                        if st.button("▶️ Run", key="run_folder_tab1_dsp"):
                            with st.spinner(f"Processing {selected_image_filename}..."):
                                answer = ask_llava(selected_image_path, selected_question)

                            output_file_for_tab1 = os.path.join(folder_path_tab1, "all_answers.txt")
                            save_response(output_file_for_tab1, selected_image_filename, selected_question, answer)

                            st.success(f"✅ Answer saved to {output_file_for_tab1}.")
                            st.text_area("📝 Answer:", answer, height=150)
                    else:
                        st.warning(f"No questions in `{base_name}.txt`.")
                else:
                    st.warning(f"⚠️ Missing question file: `{base_name}.txt`.")
        else:
            st.info("No image files found.")
    else:
        st.error("Invalid folder path.")

# ======================= TAB 2: BATCH MODE (WHOLE FOLDER) =======================
with tab2:
    st.subheader("📦 Run Batch on Whole Folder")
    st.markdown("""
    **Instructions:**
    1.  Enter folder path.
    2.  App finds images and `.txt` question files.
    3.  Each question is answered using a direct prompt.
    -   Answers saved to a **new** `all_answers.txt` **in that folder**.
    """)

    if 'folder_path_tab2' not in st.session_state:
        st.session_state.folder_path_tab2 = os.getcwd()
    batch_folder = st.text_input("Enter folder path for batch processing:", value=st.session_state.folder_path_tab2,
                                 key="fp_tab2_input_dsp")
    st.session_state.folder_path_tab2 = batch_folder

    if st.button("🚀 Run Batch Mode", key="run_batch_tab2_dsp"):
        if os.path.isdir(batch_folder):
            st.info(f"Starting batch processing for: {batch_folder}...")
            with st.spinner("Processing all images with direct prompts..."):
                run_batch_on_folder(batch_folder)
            st.success(f"✅ Batch complete. Results in {os.path.join(batch_folder, 'all_answers.txt')}.")

            try:
                with open(os.path.join(batch_folder, 'all_answers.txt'), 'r', encoding='utf-8') as f_results:
                    st.text_area("Batch Results (all_answers.txt)", f_results.read(), height=300)
            except Exception as e:
                st.warning(f"Could not display batch results: {e}")
        else:
            st.error("❌ Invalid folder path.")

# ======================= TAB 3: UPLOAD IMAGE =======================
with tab3:
    st.subheader("📥 Upload Image + Question File")
    st.markdown("""
    **Instructions:**
    1.  Upload an image (`.png`, `.jpg`, `.jpeg`).
    2.  Upload a corresponding `.txt` file containing questions (one per line).
    3.  Click "▶️ Run". Each question will be processed.
    -   Answers saved/appended to `all_answers.txt` in the `temp_uploads` directory.
    """)

    uploaded_image_file_tab3 = st.file_uploader("📤 Upload an image:", type=["png", "jpg", "jpeg"], key="img_upload_tab3_req")
    uploaded_question_file_tab3 = st.file_uploader("❓ Upload a question file (.txt):", type=["txt"], key="q_upload_tab3_req")

    if uploaded_image_file_tab3 and uploaded_question_file_tab3:
        # Save uploaded image
        uploaded_image_path = os.path.join(UPLOAD_OUTPUT_DIR, uploaded_image_file_tab3.name)
        try:
            with open(uploaded_image_path, "wb") as f:
                f.write(uploaded_image_file_tab3.getbuffer())
            st.image(uploaded_image_path, caption=f"Uploaded: {uploaded_image_file_tab3.name}", width=300)

            # Read questions from uploaded question file
            questions_str = uploaded_question_file_tab3.read().decode("utf-8")
            questions_tab3 = [q.strip() for q in questions_str.splitlines() if q.strip()]

            if not questions_tab3:
                st.warning("The uploaded question file is empty or contains no valid questions.")
            else:
                st.write("📋 Questions from file:")
                st.json(questions_tab3)

                if st.button("▶️ Run on Uploaded Image & Questions", key="run_uploaded_tab3_files_req"):
                    output_file_for_tab3 = os.path.join(UPLOAD_OUTPUT_DIR, "all_answers.txt")
                    num_questions = len(questions_tab3)
                    st.info(f"Processing {num_questions} questions for {uploaded_image_file_tab3.name}...")
                    
                    progress_bar = st.progress(0)
                    results_display_area = st.empty() # Placeholder for results
                    all_results_text = ""

                    for i, question in enumerate(questions_tab3):
                        with st.spinner(f"Asking: {question[:50]}... ({i+1}/{num_questions})"):
                            answer = ask_llava(uploaded_image_path, question)
                        save_response(output_file_for_tab3, uploaded_image_file_tab3.name, question, answer)
                        
                        current_result_text = f"Q: {question}\nA: {answer}\n---\n"
                        all_results_text += current_result_text
                        results_display_area.text_area("📝 Results (updated as processed):", all_results_text, height=max(200, len(questions_tab3)*75))
                        progress_bar.progress((i + 1) / num_questions)
                    
                    st.success(f"✅ Processed {num_questions} questions. Answers saved to {output_file_for_tab3}.")
        except Exception as e:
            st.error(f"Error handling uploaded files: {e}")
            if os.path.exists(uploaded_image_path):
                try:
                    os.remove(uploaded_image_path) # Clean up partially saved image if error
                except Exception as e_rem:
                    st.warning(f"Could not remove temp file {uploaded_image_path}: {e_rem}")

    elif uploaded_image_file_tab3 and not uploaded_question_file_tab3:
        st.info("Please upload a question file (.txt).")
    elif not uploaded_image_file_tab3 and uploaded_question_file_tab3:
        st.info("Please upload an image file.")

st.divider()
st.markdown("---")
if st.button("❌ Close Application", key="close_app_main"):
    st.stop()
st.caption("Streamlit app session active.")