
from src import memory_store


def test_save_and_load_message(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.save_message("user", "Hello")
    memory_store.save_message("assistant", "Hi!")

    history = memory_store.load_history()

    assert len(history) == 2
    assert history[0] == {
        "role": "user",
        "content": "Hello"
    }
    assert history[1] == {
        "role": "assistant",
        "content": "Hi!"
    }


def test_load_history_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.save_message("user", "First")
    memory_store.save_message("user", "Second")
    memory_store.save_message("user", "Third")

    history = memory_store.load_history(limit=2)

    assert len(history) == 2
    assert history[0]["content"] == "Second"
    assert history[1]["content"] == "Third"


def test_clear_history(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.save_message("user", "Hello")
    memory_store.save_fact("name", "Alice")

    memory_store.clear_history()

    assert memory_store.load_history() == []
    assert memory_store.load_facts()["name"] == "Alice"


def test_save_and_load_fact(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.save_fact("name", "Alice")

    facts = memory_store.load_facts()

    assert facts["name"] == "Alice"


def test_remember_name_from_message(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.remember_from_message(
        "My name is Alice"
    )

    assert memory_store.load_facts()["name"] == "Alice"


def test_remember_programming_language(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.remember_from_message(
        "My favourite programming language is Python"
    )

    facts = memory_store.load_facts()

    assert facts["favourite programming language"] == "Python"


def test_format_memory_when_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    assert memory_store.format_memory() == (
        "No personal information has been saved yet."
    )


def test_format_memory_with_facts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_store, "DB", tmp_path / "test.db"
    )

    memory_store.save_fact("name", "Alice")

    result = memory_store.format_memory()

    assert "- name: Alice" in result
