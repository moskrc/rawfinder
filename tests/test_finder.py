from pathlib import Path

from rawfinder.finder import FileFinder


class TestFileFinder:
    def test_find_files_returns_correct_files(self, sample_dir: Path) -> None:
        extensions = {".jpg", ".jpeg", ".cr2"}
        finder = FileFinder(sample_dir, extensions)
        found_files = finder.find_files()
        expected = {
            sample_dir / "image1.JPG",
            sample_dir / "image2.jpeg",
            sample_dir / "image.cr2",
            sample_dir / "subfolder" / "image3.JpEg",
        }
        assert set(found_files) == expected

    def test_find_files_no_matches(self, tmp_path: Path) -> None:
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        finder = FileFinder(empty_dir, {".txt"})
        found_files = finder.find_files()
        assert found_files == []

    def test_find_files_with_nonexistent_extension(self, sample_dir: Path) -> None:
        finder = FileFinder(sample_dir, {".png"})
        found_files = finder.find_files()
        assert found_files == []
