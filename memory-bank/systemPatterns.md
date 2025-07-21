# System Patterns: Visual Question Answering Pipeline

## 1. System Architecture

The system follows a simple, monolithic architecture with three main components:

1.  **User Interface (app.py):** A Streamlit application that serves as the front-end for user interaction.
2.  **Core Logic (helper.py):** A helper module that contains the business logic for interacting with the LLaVA model, processing data, and saving results.
3.  **Evaluation Script (generate_evaluation_text.py):** A standalone script for evaluating the model's performance.

## 2. Key Technical Decisions

*   **Local Model Execution:** The use of `ollama` allows for local execution of the LLaVA model, making the system self-contained and independent of external APIs.
*   **File-Based Data Storage:** All data, including questions, answers, and evaluation results, is stored in simple text files. This simplifies the data management process and makes the data easily accessible.
*   **Streamlit for UI:** The choice of Streamlit enables rapid development of a functional and interactive user interface with minimal code.