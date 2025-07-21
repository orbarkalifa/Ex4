# Product Context: Visual Question Answering Pipeline

## 1. Problem Solved

This project addresses the need for a simple, self-contained system to experiment with and evaluate a local Visual Question Answering (VQA) model. It provides a user-friendly interface that abstracts away the complexities of command-line tools, making it accessible to a wider audience.

## 2. How It Works

The system allows users to interact with the LLaVA model in three ways:

1.  **Single Image Mode:** Select an image and a question from a local folder to get an answer.
2.  **Batch Mode:** Process an entire folder of images and their corresponding questions in one go.
3.  **Upload Mode:** Upload an image and a text file with questions to get answers.

The application saves all answers to a text file for later review and analysis.

## 3. User Experience Goals

*   **Simplicity:** The user interface should be intuitive and easy to use, even for those unfamiliar with VQA models.
*   **Flexibility:** Support multiple modes of operation to accommodate different use cases.
*   **Transparency:** Provide clear feedback to the user during processing and save all results for easy access.