import pytest

from rawfinder.copier import FileCopier
from rawfinder.exceptions import OverwriteDisabledError
from rawfinder.integrity import FileIntegrityChecker


class TestFileCopier:
    def test_copy_file(self, tmp_path):
        src = tmp_path / "source.txt"
        dest_dir = tmp_path / "dest"
        src.write_text("Test content")
        copier = FileCopier()
        assert copier.copy(src, dest_dir) is True
        assert (dest_dir / "source.txt").read_text() == "Test content"

    def test_copy_overwrite(self, tmp_path):
        src = tmp_path / "source.txt"
        dest_dir = tmp_path / "dest"
        dest_file = dest_dir / "source.txt"
        src.write_text("New content")
        dest_file.parent.mkdir()
        dest_file.write_text("Old content")
        copier = FileCopier(overwrite=True)
        assert copier.copy(src, dest_dir) is True
        assert dest_file.read_text() == "New content"

    def test_copy_no_overwrite(self, tmp_path):
        src = tmp_path / "source.txt"
        dest_dir = tmp_path / "dest"
        dest_file = dest_dir / "source.txt"
        src.write_text("New content")
        dest_file.parent.mkdir()
        dest_file.write_text("Old content")
        copier = FileCopier(overwrite=False)
        with pytest.raises(OverwriteDisabledError):
            copier.copy(src, dest_dir)

    def test_dry_run(self, tmp_path):
        src = tmp_path / "source.txt"
        dest_dir = tmp_path / "dest"
        src.write_text("Test content")
        copier = FileCopier(dry_run=True)
        assert copier.copy(src, dest_dir) is True
        assert not (dest_dir / "source.txt").exists()

    def test_verify_copy(self, tmp_path):
        src = tmp_path / "source.txt"
        dest_dir = tmp_path / "dest"
        src.write_text("Test content")
        verifier = FileIntegrityChecker()
        copier = FileCopier(verifier=verifier)
        assert copier.copy(src, dest_dir) is True
        assert (dest_dir / "source.txt").read_text() == "Test content"
