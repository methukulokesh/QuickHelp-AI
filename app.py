import os
import streamlit as st
from dotenv import load_dotenv
from src.chat_engine import answer_question
from src.document_store import add_uploaded_documents, retrieve_context
from src.memory_store import save_message, load_history, clear_history
from src.tools import calculator

load_dotenv()
st.set_page_config(page_title="QuickHelp AI", page_icon="🤖", layout="wide")

st.title("🤖 QuickHelp AI")
st.caption("A practical AI assistant with document search, conversation memory, and utility tools.")

with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("AI provider", ["Ollama (local)", "OpenAI API"])
    if provider == "Ollama (local)":
        model = st.text_input("Ollama model", value=os.getenv("OLLAMA_MODEL", "llama3.2"))
        st.caption("Start Ollama locally and pull the selected model.")
    else:
        model = st.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
        st.caption("Set OPENAI_API_KEY in your .env file.")
    st.divider()
    st.subheader("Knowledge base")
    uploads = st.file_uploader("Upload PDF, DOCX, TXT or MD files", type=["pdf", "docx", "txt", "md"], accept_multiple_files=True)
    if st.button("Index uploaded documents", use_container_width=True):
        if uploads:
            count = add_uploaded_documents(uploads)
            st.success(f"Added {count} text chunks to the local knowledge base.")
        else:
            st.warning("Choose at least one document first.")
    st.caption("Retrieval uses local TF-IDF search; uploaded text is stored locally.")
    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        clear_history()
        st.rerun()
    st.caption("QuickHelp AI MVP • Python + Streamlit")

# Conversation display
history = load_history()
for item in history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

prompt = st.chat_input("Ask a question, or try: calculate 125 * 8")
if prompt:
    save_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Small deterministic tool route for arithmetic requests
    tool_result = None
    if prompt.lower().startswith(("calculate ", "compute ")):
        tool_result = calculator(prompt.split(" ", 1)[1])

    context = retrieve_context(prompt, top_k=4)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = answer_question(
                prompt=prompt,
                provider=provider,
                model=model,
                context=context,
                history=load_history()[-8:],
                tool_result=tool_result,
            )
        st.markdown(result)
    save_message("assistant", result)
