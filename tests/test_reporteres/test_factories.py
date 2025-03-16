import pytest

from rawfinder.exceptions import UnknownReporterError
from rawfinder.reporters.factories import ReporterFactory
from rawfinder.reporters.plain import PlainProgressReporter
from rawfinder.reporters.rich import RichProgressReporter


class ReporterFactoryTest:
    def test_create_plain_reporter(self):
        reporter = ReporterFactory.create("plain")
        assert isinstance(reporter, PlainProgressReporter)

    def test_create_rich_reporter(self):
        reporter = ReporterFactory.create("rich")
        assert isinstance(reporter, RichProgressReporter)

    def test_invalid_reporter_type(self):
        with pytest.raises(UnknownReporterError, match="Reporter type 'invalid' is not supported"):
            ReporterFactory.create("invalid")
