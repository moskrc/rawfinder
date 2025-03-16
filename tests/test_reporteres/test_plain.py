from rawfinder.reporters.plain import PlainProgressReporter


class PlainProgressReporterTest:
    def test_start(self, caplog):
        reporter = PlainProgressReporter()
        with caplog.at_level("INFO"):
            reporter.start(10, "Processing")
            assert "Processing [0/10]" in caplog.text

    def test_update(self, caplog):
        reporter = PlainProgressReporter()
        reporter.start(10, "Processing")
        with caplog.at_level("INFO"):
            reporter.update("File 1", advance=1)
            assert "[1/10] File 1" in caplog.text

    def test_complete(self, caplog):
        reporter = PlainProgressReporter()
        reporter.start(10, "Processing")
        reporter.current = 10
        with caplog.at_level("INFO"):
            reporter.complete()
            assert "Completed 10/10 files" in caplog.text
