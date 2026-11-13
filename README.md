# QuickHelp AI

QuickHelp AI is a Python + Streamlit assistant MVP that combines an LLM chat interface, local document retrieval (RAG-style), SQLite conversation history, and a safe arithmetic tool.

## Features

- Chat interface built with Streamlit.
- Choose a local Ollama model or OpenAI API from the sidebar.
- Upload PDF, DOCX, TXT, and Markdown files.
- Extract and chunk documents, then retrieve relevant passages with TF-IDF similarity.
- Persist conversation messages in SQLite.
- Basic arithmetic tool uses Python AST parsing (not `eval`).
- Clear conversation history from the sidebar.

## Architecture

```text
Streamlit UI (app.py)
   |-- Chat engine (src/chat_engine.py) ---- Ollama / OpenAI
   |-- Document store (src/document_store.py) -- TF-IDF retrieval
   |-- Memory store (src/memory_store.py) ----- SQLite
   |-- Utility tool (src/tools.py) ------------ safe calculator
```

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   Windows PowerShell:
   ```powershell
   py -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`. For OpenAI, add your API key. Never commit `.env`.
6. Start the app:
   ```powershell
   streamlit run app.py
   ```

### Local Ollama option

Install Ollama separately, then run:
```powershell
ollama pull llama3.2
ollama serve
```
Choose **Ollama (local)** in the app sidebar. Ollama must be running on the same machine.

### OpenAI option

Set `OPENAI_API_KEY` in `.env`, run the app, and select **OpenAI API** in the sidebar. API usage may incur charges.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Current MVP scope and limitations

- TF-IDF is a lightweight lexical retrieval baseline, not a vector database or embedding model.
- The model provider must be configured by the user; this repository does not include an API key or bundled LLM.
- PDF extraction works for text-based PDFs; scanned PDFs need OCR, which is not included.
- This is a local learning/portfolio MVP, not a production-hardened service. Authentication, deployment, role-based access, and advanced agent planning are not included.

## Project objective

Demonstrate how an AI assistant can combine language-model responses, retrieval from user-provided documents, persistent conversation history, and a small deterministic tool in one usable application.
