from pathlib import Path

from rawfinder.matcher import FileMatcher


class TestFileMatcher:
    def test_get_matching_raw_found(self, tmp_path: Path) -> None:
        raw_file1 = tmp_path / "photo1.raw"
        raw_file1.touch()
        raw_file2 = tmp_path / "photo2.raw"
        raw_file2.touch()

        matcher = FileMatcher([raw_file1, raw_file2])

        jpeg_file = tmp_path / "PHOTO1.jpg"
        matching = matcher.get_matching_raw(jpeg_file)

        assert matching == raw_file1, "Should return the RAW file corresponding to 'photo1'"

    def test_get_matching_raw_not_found(self, tmp_path: Path) -> None:
        raw_file = tmp_path / "file.raw"
        raw_file.touch()
        matcher = FileMatcher([raw_file])

        jpeg_file = tmp_path / "nonexistent.jpg"
        matching = matcher.get_matching_raw(jpeg_file)

        assert matching is None, "Should return None when there is no matching RAW file"

    def test_case_insensitivity(self, tmp_path: Path) -> None:
        raw_file = tmp_path / "Test.RAW"
        raw_file.touch()
        matcher = FileMatcher([raw_file])

        jpeg_file = tmp_path / "test.jpeg"
        matching = matcher.get_matching_raw(jpeg_file)

        assert matching == raw_file, "Matching should be case-insensitive"

    def test_duplicate_raw_files(self, tmp_path: Path) -> None:
        raw_file1 = tmp_path / "duplicate.raw"
        raw_file1.touch()
        raw_file2 = tmp_path / "duplicate.DNG"
        raw_file2.touch()

        matcher = FileMatcher([raw_file1, raw_file2])

        jpeg_file = tmp_path / "duplicate.jpg"
        matching = matcher.get_matching_raw(jpeg_file)

        assert matching == raw_file1, "Should return the first matching RAW file when duplicates are present"
