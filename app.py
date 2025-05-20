import streamlit as st
import os
from helper import ask_llava, save_response, run_batch_on_folder

st.set_page_config(page_title="LLaVA Image Analyzer", layout="centered")

st.markdown("# 🧠 LLaVA:7b – Visual Question Answering")
st.markdown("Use this app to analyze images and generate answers using only the visible content, powered by `llava:7b`.")
st.divider()

tab1, tab2, tab3 = st.tabs(["📂 Folder Mode", "📦 Batch Mode", "📥 Upload Image"])

# ======================= TAB 1: FOLDER MODE =======================
with tab1:
    st.subheader("📂 Folder-Based Image + Question")
    st.markdown("""
**Instructions:**
- Your folder must include:
  - Images with names starting with `drawing_`, `text_`, or `flowchart_`
  - A `.txt` file with the same base name for each image
- Select an image and a question.
- The answer will be saved in `all_answers.txt` in that folder.
    """)

    folder_path = st.text_input("Enter folder path:", value=os.getcwd())

    if os.path.isdir(folder_path):
        image_files = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])

        if image_files:
            selected_image = st.selectbox("🖼️ Select image", image_files)
            selected_image_path = os.path.abspath(os.path.join(folder_path, selected_image))
            st.image(selected_image_path, caption=selected_image, width=300)

            name = os.path.splitext(selected_image)[0]
            question_file = os.path.join(folder_path, f"{name}.txt")

            if os.path.exists(question_file):
                with open(question_file, "r", encoding="utf-8") as f:
                    questions = [line.strip() for line in f if line.strip()]
                if questions:
                    selected_question = st.selectbox("📋 Select a question", questions)
                    if st.button("▶️ Run", key="run_folder"):
                        answer = ask_llava(selected_image_path, selected_question)
                        save_response(selected_image_path, selected_question, answer)
                        st.success("✅ Answer saved to all_answers.txt.")
                        st.text_area("📝 Answer:", answer, height=200)
            else:
                st.warning(f"⚠️ Missing file: `{name}.txt`")
        else:
            st.warning("No images found in the selected folder.")

# ======================= TAB 2: BATCH MODE =======================
with tab2:
    st.subheader("📦 Run Batch on Folder")
    st.markdown("""
**Instructions:**
- This will match each image with its `.txt` file based on name.
- Answers for all valid pairs will be saved into `all_answers.txt` inside the folder.
    """)

    batch_folder = st.text_input("Enter folder path for batch processing:", value=os.getcwd())

    if st.button("🚀 Run Batch Mode"):
        if os.path.isdir(batch_folder):
            run_batch_on_folder(batch_folder)
            st.success("✅ Batch complete. Saved to all_answers.txt.")
        else:
            st.error("❌ Invalid folder path.")

# ======================= TAB 3: UPLOAD MODE =======================
with tab3:
    st.subheader("📥 Upload Image + Manual Question")
    st.markdown("""
**Instructions:**
- Upload an image (`.png`, `.jpg`, `.jpeg`)
- Enter a question about the image
- The model will automatically infer the image type based on its name (`drawing_`, `text_`, `flowchart_`)
    """)

    uploaded_file = st.file_uploader("📤 Upload an image:", type=["png", "jpg", "jpeg"])
    manual_question = st.text_input("❓ Enter your question:")

    if uploaded_file and manual_question:
        os.makedirs("temp_uploads", exist_ok=True)
        file_path = os.path.abspath(os.path.join("temp_uploads", uploaded_file.name))

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.image(file_path, caption=uploaded_file.name, width=300)

        if st.button("▶️ Run on Uploaded Image", key="run_uploaded"):
            answer = ask_llava(file_path, manual_question)
            save_response(file_path, manual_question, answer)
            st.success("✅ Answer saved to all_answers.txt.")
            st.text_area("📝 Answer:", answer, height=200)

# ========== Exit ==========
st.divider()
if st.button("❌ Close App"):
    st.stop()
