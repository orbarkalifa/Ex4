import streamlit as st
import os
from helper import ask_llava

st.set_page_config(page_title="LLaVA Q&A", layout="centered")
st.title("Image Question Answering using LLaVA:7b")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
question = st.text_input("Enter your question")

if uploaded_file and question:
    os.makedirs("temp", exist_ok=True)
    img_path = os.path.abspath(os.path.join("temp", uploaded_file.name))
    with open(img_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(img_path, caption="Uploaded Image", use_container_width=True)

    if st.button("Run"):
        answer = ask_llava(img_path, question)
        st.subheader("Answer")
        st.text_area("LLaVA Output", answer, height=200)
