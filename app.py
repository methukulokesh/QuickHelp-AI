
import os
import streamlit as st
from dotenv import load_dotenv

from src.chat_engine import answer_question
from src.document_store import add_uploaded_documents, retrieve_context
from src.memory_store import (
    save_message,
    load_history,
    clear_history,
    remember_from_message,
    format_memory,
)
from src.tools import calculator

load_dotenv()

st.set_page_config(
    page_title="QuickHelp AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 QuickHelp AI")
st.caption(
    "A practical AI assistant with document search, "
    "persistent personal memory, and utility tools."
)

# Sidebar settings
with st.sidebar:
    st.header("Settings")

    provider = st.selectbox(
        "AI provider",
        ["Ollama (local)", "OpenAI API"]
    )

    if provider == "Ollama (local)":
        model = st.text_input(
            "Ollama model",
            value=os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        )
        st.caption("Start Ollama locally and pull the selected model.")
    else:
        model = st.text_input(
            "OpenAI model",
            value=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        )
        st.caption("Set OPENAI_API_KEY in your .env file.")

    st.divider()

    st.subheader("Knowledge base")

    uploads = st.file_uploader(
        "Upload PDF, DOCX, TXT or MD files",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True
    )

    if st.button("Index uploaded documents", use_container_width=True):
        if uploads:
            count = add_uploaded_documents(uploads)
            st.success(
                f"Added {count} text chunks to the local knowledge base."
            )
        else:
            st.warning("Choose at least one document first.")

    st.caption("Retrieval uses local TF-IDF search.")

    st.divider()

    # Persistent personal memory
    st.subheader("Personal Memory")

    st.markdown(format_memory())

    if st.button("Clear conversation", use_container_width=True):
        clear_history()
        st.rerun()

    st.caption(
        "Clearing conversation does not delete personal memory."
    )

# Display conversation history
history = load_history()

for item in history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

# Chat input
prompt = st.chat_input("Ask a question, or try: calculate 125 * 8")

if prompt:

    # Save the user's message
    save_message("user", prompt)

    # Extract and save supported personal facts
    remember_from_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Calculator tool
    tool_result = None

    if prompt.lower().startswith(("calculate ", "compute ")):
        tool_result = calculator(prompt.split(" ", 1)[1])

    # Retrieve relevant document context
    context = retrieve_context(prompt, top_k=4)

    # Load persistent personal memory
    personal_memory = format_memory()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            result = answer_question(
                prompt=prompt,
                provider=provider,
                model=model,
                context=context,
                history=load_history()[-9:-1],
                tool_result=tool_result,
                memory=personal_memory,
            )

        st.markdown(result)

    # Save assistant response
    save_message("assistant", result)
