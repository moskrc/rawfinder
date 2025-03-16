import pytest


@pytest.fixture
def sample_files(tmp_path):
    files = {
        "photo1": tmp_path / "image1.jpg",
        "photo2": tmp_path / "image2.jpg",
        "source1": tmp_path / "image1.raw",
        "source2": tmp_path / "image2.raw",
        "text": tmp_path / "document.txt",
    }
    for file in files.values():
        file.touch()

    return files


@pytest.fixture
def config_file(tmp_path):
    config_content = """
    verify_checksum_chunk_size: 8192
    reporter: plain
    dry_run: false
    verify_checksum: true
    overwrite: false
    extensions:
      photos:
        - .jpg
        - .jpeg
      sources:
        - .raw
        - .cr2
    """
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_content)
    return config_path
