import io, json, re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).resolve().parents[1]
STORE = BASE / "data" / "documents" / "knowledge_chunks.json"

def _extract(upload):
    name = upload.name.lower()
    raw = upload.getvalue()
    if name.endswith((".txt", ".md")):
        return raw.decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def _chunks(text, size=850, overlap=120):
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    result, start = [], 0
    while start < len(clean):
        end = min(start + size, len(clean))
        result.append(clean[start:end])
        if end == len(clean):
            break
        start = max(end - overlap, start + 1)
    return result

def add_uploaded_documents(uploads):
    STORE.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else []
    added = 0
    for upload in uploads:
        text = _extract(upload)
        for index, chunk in enumerate(_chunks(text)):
            existing.append({"source": upload.name, "chunk": index, "text": chunk})
            added += 1
    STORE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return added

def retrieve_context(query, top_k=4):
    if not STORE.exists():
        return ""
    records = json.loads(STORE.read_text(encoding="utf-8"))
    if not records:
        return ""
    corpus = [item["text"] for item in records]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform(corpus + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    except ValueError:
        return ""
    ranked = scores.argsort()[::-1][:top_k]
    passages = []
    for idx in ranked:
        if scores[idx] > 0:
            rec = records[int(idx)]
            passages.append(f"[Source: {rec['source']}, chunk {rec['chunk']}] {rec['text']}")
    return "\n\n".join(passages)
