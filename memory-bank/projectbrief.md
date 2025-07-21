# Project Brief: Visual Question Answering Pipeline

## 1. Overview

This project is a self-contained Visual Question Answering (VQA) system that uses a local LLaVA model to answer questions about images. It includes a web-based user interface for interactive use, batch processing capabilities for handling multiple images, and an evaluation script to measure the model's performance against a ground truth dataset.

## 2. Core Features

*   **VQA Model Integration:** Utilizes a local LLaVA model via the `ollama` command-line tool.
*   **Web Interface:** A Streamlit application provides a user-friendly UI for single-image analysis, batch processing, and image uploads.
*   **Dynamic Prompting:** The system generates type-specific prompts for different image categories (drawings, flowcharts, text) to improve accuracy.
*   **Batch Processing:** A script allows for automated processing of entire folders of images and their corresponding questions.
*   **Evaluation Framework:** A script compares the model's answers to a ground truth dataset and generates a text file for performance analysis.

## 3. Key Technologies

*   **Python:** The core programming language.
*   **Streamlit:** For the web-based user interface.
*   **Ollama:** To run the local LLaVA model.
*   **Pandas & Numpy:** For data manipulation (though not heavily used in the core logic).
*   **Pillow:** For image processing.