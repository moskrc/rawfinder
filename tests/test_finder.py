import pytest

from rawfinder.exceptions import FinderDirectoryDoesNotExistError, FinderNoExtensionError
from rawfinder.finder import FileFinder


class TestFileFinder:
    def test_init_non_existent_directory(self, tmp_path):
        non_existent = tmp_path / "non_existent"
        with pytest.raises(FinderDirectoryDoesNotExistError):
            FileFinder(non_existent, {".jpg"})

    def test_init_empty_extensions(self, tmp_path):
        with pytest.raises(FinderNoExtensionError):
            FileFinder(tmp_path, set())

    def test_find_files(self, sample_files):
        finder = FileFinder(sample_files["photo1"].parent, {".jpg", ".raw"})
        files = finder.find_files()
        assert len(files) == 4  # image1.jpg, image2.jpg, image1.raw, image2.raw
        assert {f.name for f in files} == {"image1.jpg", "image2.jpg", "image1.raw", "image2.raw"}

    def test_find_files_no_matches(self, tmp_path):
        (tmp_path / "document.txt").touch()
        finder = FileFinder(tmp_path, {".jpg", ".raw"})
        files = finder.find_files()
        assert len(files) == 0

    def test_find_files_case_insensitivity(self, tmp_path):
        (tmp_path / "image1.JPG").touch()
        (tmp_path / "image2.RAW").touch()
        finder = FileFinder(tmp_path, {".jpg", ".raw"})
        files = finder.find_files()
        assert len(files) == 2
        assert {f.name for f in files} == {"image1.JPG", "image2.RAW"}
