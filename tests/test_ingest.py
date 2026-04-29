import pytest
from ingest import ingest


@pytest.fixture
def temp_dirs(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    vs_dir = tmp_path / "vectorstore"
    (data_dir / "qa.txt").write_text(
        "Q: Why do you want to work at Commerzbank?\n"
        "A: I am passionate about applying data science to real-world financial problems.\n"
        "Q: What is your background?\n"
        "A: I studied data science and have experience with Python and machine learning."
    )
    monkeypatch.setattr("ingest.DATA_DIR", str(data_dir))
    monkeypatch.setattr("ingest.VECTORSTORE_DIR", str(vs_dir))
    return data_dir, vs_dir


def test_ingest_creates_vectorstore(temp_dirs):
    _, vs_dir = temp_dirs
    ingest()
    assert vs_dir.exists()
    assert any(vs_dir.iterdir())


def test_ingest_fails_on_empty_data_dir(monkeypatch, tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.setattr("ingest.DATA_DIR", str(empty_dir))
    monkeypatch.setattr("ingest.VECTORSTORE_DIR", str(tmp_path / "vs"))
    with pytest.raises(ValueError, match="No documents found"):
        ingest()
