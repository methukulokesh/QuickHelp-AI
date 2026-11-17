
import io
import json

from src import document_store


class FakeUpload:
    def __init__(self, name, content):
        self.name = name
        self._content = content

    def getvalue(self):
        return self._content


def test_extract_txt():
    upload = FakeUpload(
        "notes.txt",
        b"QuickHelp AI uses Python and Streamlit."
    )

    result = document_store._extract(upload)

    assert "QuickHelp AI" in result
    assert "Python" in result


def test_chunks_text():
    text = "A" * 2000

    chunks = document_store._chunks(
        text, size=500, overlap=100
    )

    assert len(chunks) > 1
    assert chunks[0][-100:] == chunks[1][:100]


def test_chunks_empty_text():
    assert document_store._chunks("   ") == []


def test_add_uploaded_document(tmp_path, monkeypatch):
    monkeypatch.setattr(
        document_store,
        "STORE",
        tmp_path / "knowledge_chunks.json"
    )

    upload = FakeUpload(
        "notes.txt",
        b"Python is a programming language."
    )

    count = document_store.add_uploaded_documents([upload])

    assert count == 1

    records = json.loads(
        document_store.STORE.read_text(encoding="utf-8")
    )

    assert records[0]["source"] == "notes.txt"
    assert "Python" in records[0]["text"]


def test_duplicate_upload_replaces_old_content(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        document_store,
        "STORE",
        tmp_path / "knowledge_chunks.json"
    )

    first = FakeUpload("notes.txt", b"Old content about Java.")
    second = FakeUpload("notes.txt", b"New content about Python.")

    document_store.add_uploaded_documents([first])
    document_store.add_uploaded_documents([second])

    records = json.loads(
        document_store.STORE.read_text(encoding="utf-8")
    )

    assert len(records) == 1
    assert "Python" in records[0]["text"]
    assert "Java" not in records[0]["text"]


def test_retrieve_relevant_context(tmp_path, monkeypatch):
    monkeypatch.setattr(
        document_store,
        "STORE",
        tmp_path / "knowledge_chunks.json"
    )

    upload = FakeUpload(
        "notes.txt",
        b"Python is a programming language used for data science."
    )

    document_store.add_uploaded_documents([upload])

    result = document_store.retrieve_context(
        "Python programming language"
    )

    assert "Python" in result
    assert "notes.txt" in result


def test_retrieve_empty_query(tmp_path, monkeypatch):
    monkeypatch.setattr(
        document_store,
        "STORE",
        tmp_path / "knowledge_chunks.json"
    )

    assert document_store.retrieve_context("   ") == ""


def test_retrieve_without_knowledge_base(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        document_store,
        "STORE",
        tmp_path / "missing.json"
    )

    assert document_store.retrieve_context("Python") == ""
