from rawfinder.matcher import FileMatcher


class TestFileMatcher:
    def test_index_sources(self, sample_files):
        source_files = [sample_files["source1"], sample_files["source2"]]
        matcher = FileMatcher(source_files)
        matcher._index_sources()
        assert matcher._index == {"image1": sample_files["source1"], "image2": sample_files["source2"]}

    def test_get_matching_source(self, sample_files):
        source_files = [sample_files["source1"]]
        matcher = FileMatcher(source_files)
        photo_file = sample_files["photo1"]
        assert matcher.get_matching_source(photo_file) == sample_files["source1"]

    def test_no_matching_source(self, sample_files):
        source_files = [sample_files["source1"]]
        matcher = FileMatcher(source_files)
        photo_file = sample_files["photo2"]
        assert matcher.get_matching_source(photo_file) is None
