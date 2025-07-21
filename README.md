# Visual Question Answering Pipeline

A user-friendly tool for exploring and evaluating local Visual Question Answering (VQA) models.

## 🌟 Overview

Visual Question Answering Pipeline is a Streamlit-based application that provides an intuitive interface for interacting with local VQA models like LLaVA. It allows users to ask questions about images through a web UI, process entire folders of images in batch mode, and evaluate model performance against a ground-truth dataset. The system is designed to be self-contained and easy to use, making it ideal for researchers, developers, and enthusiasts who want to experiment with VQA models without relying on external APIs.

## ✨ Features

*   **Interactive UI:** A simple and intuitive web interface built with Streamlit.
*   **Multiple Modes:** Supports single image analysis, batch processing of folders, and direct image uploads.
*   **Local Model Support:** Integrates with local VQA models through `ollama`.
*   **Dynamic Prompting:** Tailors prompts based on image type (e.g., drawings, flowcharts, text) to improve accuracy.
*   **Evaluation Script:** Includes a script to compare model answers against a ground-truth dataset.

## 🚀 Getting Started

### Prerequisites

*   Python 3.8+
*   Ollama installed and running.
*   A LLaVA model (e.g., `llava:7b`) pulled into your Ollama library:
    ```bash
    ollama pull llava:7b
    ```

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  Launch the Streamlit app:
    ```bash
    streamlit run app.py
    ```
2.  Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## 🔧 How to Use

The application has three main tabs:

### 📂 Folder Mode (Single Image)

1.  Enter the path to a folder containing images and corresponding `.txt` question files.
2.  Select an image and a question from the dropdown menus.
3.  Click "▶️ Run" to get the answer.

### 📦 Batch Mode (Whole Folder)

1.  Enter the path to a folder containing images and question files.
2.  Click "🚀 Run Batch Mode" to process all images in the folder.
3.  The results will be saved to `all_answers.txt` in the specified folder.

### 📥 Upload Image

1.  Upload an image file (`.png`, `.jpg`, `.jpeg`).
2.  Upload a `.txt` file containing one question per line.
3.  Click "▶️ Run" to process the image with all questions.

## 📊 Evaluation

To evaluate the model's performance:

1.  First, run the batch mode on the `pics_and_questions` folder to generate an `all_answers.txt` file.
2.  Then, run the evaluation script:
    ```bash
    python generate_evaluation_text.py
    ```
3.  This will create an `evaluation_input_for_chatgpt.txt` file, which you can use to get a performance score from a large language model.

## 📂 Project Structure

```
.
├── app.py                      # Main Streamlit application
├── helper.py                   # Core logic for interacting with the VQA model
├── generate_evaluation_text.py # Script for generating the evaluation text
├── process_all.py              # (Assumed utility script)
├── requirements.txt            # Python dependencies
├── pics_and_questions/         # Example images and questions
│   ├── drawing_...
│   └── ...
├── memory-bank/                # Project documentation
│   ├── projectbrief.md
│   └── ...
└── README.md