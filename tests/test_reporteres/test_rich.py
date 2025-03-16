from rawfinder.reporters.rich import RichProgressReporter


class RichProgressReporterTest:
    def test_start(self):
        reporter = RichProgressReporter()
        reporter.start(10, "Processing")
        assert reporter.total == 10
        assert reporter.description == "Processing"

    def test_update(self, capsys):
        reporter = RichProgressReporter()
        reporter.start(10, "Processing")
        reporter.update("File 1", advance=1)
        assert reporter.current == 1

    def test_complete(self):
        reporter = RichProgressReporter()
        reporter.start(10, "Processing")
        reporter.current = 10
        reporter.complete()
        assert reporter.current == 10
