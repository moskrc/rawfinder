import pytest

from rawfinder.app import RawFinderApp
from rawfinder.copier import FileCopier
from rawfinder.reporters.plain import PlainProgressReporter


class TestRawFinderApp:
    def test_validate_directories(self, tmp_path):
        non_existent = tmp_path / "non_existent"
        with pytest.raises(Exception, match="Directory .* does not exist"):
            RawFinderApp(non_existent, tmp_path, tmp_path, FileCopier(), PlainProgressReporter())

    def test_confirm_copy_yes(self, tmp_path, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "y")
        app = RawFinderApp(tmp_path, tmp_path, tmp_path, FileCopier(), PlainProgressReporter())
        assert app._confirm_copy([("photo.jpg", "source.raw")]) is True
