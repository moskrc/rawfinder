from pathlib import PosixPath

from rawfinder.finders import JpegFinder, BaseFinder, RawFinder


class TestBaseFinder:
    def test_convert_to_case_insensitive(self):
        res = BaseFinder._convert_to_case_insensitive(".txt")
        assert res == "*.[tT][xX][tT]"

    def test_get_image_files(self, generate_files):
        """It should be able to find necessary files"""
        file_data = [(5, "TXT"), (10, "bmp"), (15, "mp3")]
        temp_dir = generate_files(file_data)

        class CustomFinder(BaseFinder):
            extensions = [
                ".txt",
                ".bmp",
            ]

        res = CustomFinder(temp_dir).find()
        assert len(res) == 15
        assert type(res.pop()) is PosixPath

    def test_get_image_files_doesnt_exists(self, generate_files):
        file_data = [(5, "txt"), (10, "bmp"), (15, "AVI")]
        temp_dir = generate_files(file_data)

        class CustomFinder(BaseFinder):
            extensions = [
                ".mpeg",
            ]

        res = CustomFinder(temp_dir).find()
        assert len(res) == 0


class TestJpegFinder:
    def test_get_image_files(self, generate_files):
        """It should be able to find necessary files"""
        file_data = [(3, "jpg"), (4, "jPeG"), (5, "mp3"), (1, "avi")]
        temp_dir = generate_files(file_data)

        res = JpegFinder.find(temp_dir)
        assert len(res) == 7


class TestRawFinder:
    def test_extensions(self):
        assert RawFinder.extensions == [
            ".cr2",
            ".nef",
            ".dng",
            ".arw",
            ".raf",
            ".rw2",
            ".orf",
            ".srw",
            ".pef",
            ".x3f",
            ".sr2",
        ]

    def test_get_image_files(self, generate_files):
        """It should be able to find necessary files"""
        file_data = [
            (3, "sr2"),
            (4, "cr2"),
            (5, "nef"),
        ]
        temp_dir = generate_files(file_data)

        res = RawFinder.find(temp_dir)
        assert len(res) == 12
