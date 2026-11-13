# QuickHelp AI – Project Overview

## Problem
Users often need one interface to ask general questions, search their own notes/documents, and perform small utility tasks.

## Solution
QuickHelp AI provides a Streamlit chat interface backed by a configurable LLM provider. Uploaded documents are extracted and split into chunks; TF-IDF similarity retrieves relevant passages for the model. SQLite stores chat messages between app reruns. A restricted arithmetic parser handles simple calculations without executing arbitrary Python.

## Main components
- UI: Streamlit
- LLM integration: OpenAI Chat Completions or Ollama chat endpoint
- Retrieval: scikit-learn TF-IDF + cosine similarity
- Memory: SQLite
- Tool: AST-based arithmetic evaluator

## Data flow
1. User submits a message.
2. The app checks whether it is a calculator request.
3. The document store retrieves the most relevant chunks.
4. Chat history and retrieved context are sent to the selected model.
5. The answer is displayed and persisted in SQLite.

## Security and limitations
API keys are read from environment variables and should never be committed. Arithmetic parsing allows only numeric constants and a small set of arithmetic operators. Uploaded document text is stored locally. This MVP does not include user authentication or production security controls.
