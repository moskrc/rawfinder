from rawfinder.exceptions import UnknownReporterError
from rawfinder.reporters import ProgressReporter
from rawfinder.reporters.plain import PlainProgressReporter
from rawfinder.reporters.rich import RichProgressReporter


class ReporterFactory:
    @staticmethod
    def create(reporter_type: str = "rich") -> ProgressReporter:
        reporters = {
            "plain": PlainProgressReporter,
            "rich": RichProgressReporter,
        }
        try:
            return reporters[reporter_type.lower()]()
        except KeyError as e:
            raise UnknownReporterError(reporter_type) from e
