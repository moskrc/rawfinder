from pathlib import Path

import pytest

from rawfinder.copier import AsyncFileCopier


@pytest.fixture
def copier() -> AsyncFileCopier:
    return AsyncFileCopier()


@pytest.fixture
def sample_dir(tmp_path: Path) -> Path:
    base = tmp_path / "sample"
    base.mkdir()
    (base / "image1.JPG").write_text("image data")
    (base / "image2.jpeg").write_text("image data")
    (base / "image.cr2").write_text("image CR2")
    (base / "document.pdf").write_text("document data")
    (base / "script.py").write_text("print('Hello')")
    sub = base / "subfolder"
    sub.mkdir()
    (sub / "image3.JpEg").write_text("image data")
    (sub / "notes.txt").write_text("notes")
    return base
