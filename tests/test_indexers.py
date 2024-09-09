from pathlib import Path

from rawfinder.indexers import FileStorage


class TestDictIndexer:
    def test_index(self):
        indexer = FileStorage()
        assert not indexer.indexed
        test_files = [
            Path("/DCIM/IMG_2101.CR2"),
            Path("/DCIM/IMG_2102.CR2"),
            Path("/DCIM/OLD/IMG_2101.CR2"),
            Path("Gamma12.bmp"),
        ]
        indexer.make_index(test_files)
        assert indexer.indexed
        assert indexer._storage == {
            "gamma12": Path("Gamma12.bmp"),
            "img_2101": Path("/DCIM/OLD/IMG_2101.CR2"),
            "img_2102": Path("/DCIM/IMG_2102.CR2"),
        }
