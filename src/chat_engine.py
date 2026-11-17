
import os
import requests

SYSTEM_PROMPT = """You are QuickHelp AI, a concise and helpful general-purpose assistant.

Use the supplied personal memory to answer questions about the user.
Treat saved personal memory as information that persists across conversations.
Do not claim to remember information that is not present in the memory.

Use supplied document context when relevant.
If the answer is not present in the documents, say so and answer from general knowledge only when appropriate.

Never invent facts, sources, or actions.
For high-stakes topics, encourage checking qualified sources."""


def answer_question(
    prompt,
    provider,
    model,
    context="",
    history=None,
    tool_result=None,
    memory=""
):
    if tool_result is not None:
        return f"**Calculator result:** {tool_result}"

    history = history or []

    context_block = (
        f"\n\nDOCUMENT CONTEXT:\n{context}"
        if context
        else "\n\nNo relevant document passages were retrieved."
    )

    memory_block = (
        f"\n\nPERSISTENT PERSONAL MEMORY:\n{memory}"
        if memory
        else "\n\nNo personal memories have been saved."
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + context_block + memory_block
        }
    ]

    for item in history:
        if item.get("role") in ("user", "assistant"):
            messages.append({
                "role": item["role"],
                "content": item["content"]
            })

    messages.append({
        "role": "user",
        "content": prompt
    })

    if provider.startswith("Ollama"):
        base = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        )

        try:
            response = requests.post(
                f"{base}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=120,
            )

            response.raise_for_status()

            return response.json()["message"]["content"]

        except requests.RequestException as exc:
            return (
                "**Ollama connection failed.** "
                "Make sure Ollama is running and the model is installed.\n\n"
                f"Try: `ollama pull {model}` and `ollama serve`\n\n"
                f"Technical detail: {exc}"
            )

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "OpenAI API key not found. Add "
            "`OPENAI_API_KEY=your_key` to the `.env` file, "
            "or switch to Ollama."
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3
        )

        return (
            response.choices[0].message.content
            or "I couldn't generate a response."
        )

    except Exception as exc:
        return f"OpenAI request failed: {exc}"
