# QuickHelp AI 🤖

QuickHelp AI is a Python-based conversational AI assistant built using Streamlit. It combines local Large Language Model (LLM) integration, document-based question answering, persistent conversation history, personal memory, and a safe arithmetic calculator in one application.

## Features

- **AI Chat Interface:** Interactive conversational interface built using Streamlit.
- **Multiple LLM Providers:** Supports local Ollama models and the OpenAI API.
- **Document Upload:** Supports PDF, DOCX, TXT, and Markdown files.
- **Document Retrieval (RAG-style):** Extracts and chunks document content and retrieves relevant passages using TF-IDF similarity.
- **Conversation History:** Stores conversation messages persistently using SQLite.
- **Personal Memory:** Stores supported personal facts for use in future conversations.
- **Safe Calculator:** Performs arithmetic operations using Python AST parsing instead of `eval()`.
- **Clear History:** Allows users to clear conversation history from the sidebar.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | User interface |
| Ollama | Local LLM integration |
| Qwen 2.5 3B | Tested local language model |
| OpenAI API | Optional cloud LLM provider |
| SQLite | Conversation history and personal memory |
| Scikit-learn | TF-IDF document retrieval |
| PyPDF | PDF text extraction |
| python-docx | DOCX text extraction |

## Architecture

```text
                       User
                         |
                    Streamlit UI
                      (app.py)
                         |
          +--------------+--------------+
          |              |              |
      Chat Engine   Document Store  Memory Store
          |              |              |
       Ollama/API    TF-IDF Search    SQLite
          |
      AI Response

                  Utility Tool
                    tools.py
                 Safe Calculator
```

## Project Structure

```text
QuickHelp-AI/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── chat_engine.py
│   ├── document_store.py
│   ├── memory_store.py
│   └── tools.py
│
├── tests/
│   ├── test_tools.py
│   ├── test_memory_store.py
│   └── test_document_store.py
│
├── data/
│   └── documents/
│
└── memory/
    └── chat_history.db
```

*Note: Runtime data files and folders are created by the application when needed.*

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/methukulokesh/QuickHelp-AI.git
cd QuickHelp-AI
```

### 2. Create a virtual environment

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

For optional OpenAI integration, add your API key to `.env`.

Example configuration:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

OLLAMA_MODEL=qwen2.5:3b
OLLAMA_BASE_URL=http://localhost:11434
```

Never commit your `.env` file or expose API keys.

## Running with Ollama (Local)

1. Install Ollama from https://ollama.com/
2. Download the tested model:

```powershell
ollama pull qwen2.5:3b
```

3. Start the application:

```powershell
streamlit run app.py
```

4. Select **Ollama (local)** in the application sidebar.

Ollama must be running on the same machine as the application.

## Running with OpenAI API (Optional)

1. Configure `OPENAI_API_KEY` in your `.env` file.
2. Start the application.
3. Select **OpenAI API** in the sidebar.

OpenAI API usage may incur charges depending on account credits and pricing.

## Running Tests

Run the automated test suite:

```powershell
py -3.13 -m pytest -v
```

The project includes tests for calculator operations, personal memory, and document retrieval.

## Current MVP Scope and Limitations

- TF-IDF is a lightweight lexical retrieval baseline, not an embedding-based vector database.
- The application requires a configured and accessible LLM provider to generate AI responses.
- PDF extraction supports text-based PDFs; scanned PDFs require OCR, which is not included.
- A locally running Ollama server is not directly accessible to a separately hosted cloud application.
- Authentication, role-based access, production deployment hardening, and advanced agent planning are not included.

## Project Objective

The objective of QuickHelp AI is to demonstrate how an AI assistant can combine language-model responses, retrieval from user-provided documents, persistent conversation history, personal memory, and deterministic utility tools in one usable application.

## Author

Developed as a practical AI assistant project using Python and open-source technologies.

**GitHub:** https://github.com/methukulokesh/QuickHelp-AI