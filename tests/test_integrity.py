import hashlib

import pytest

from rawfinder.exceptions import ChecksumError
from rawfinder.integrity import FileIntegrityChecker


class TestFileIntegrityChecker:
    def test_calculate_hash(self, tmp_path):
        file = tmp_path / "test.txt"
        file.write_text("Hello, world!")
        checker = FileIntegrityChecker()
        hash_value = checker.calculate_hash(file)
        assert hash_value == hashlib.sha256(b"Hello, world!").hexdigest()

    def test_verify_copy_identical(self, tmp_path):
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("Same content")
        file2.write_text("Same content")
        checker = FileIntegrityChecker()
        checker.verify_copy(file1, file2)

    def test_verify_copy_different(self, tmp_path):
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("Content A")
        file2.write_text("Content B")
        checker = FileIntegrityChecker()
        with pytest.raises(ChecksumError):
            checker.verify_copy(file1, file2)
