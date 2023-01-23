import argparse
import os
import pathlib

DEFAULT_DST_FOLDER = "raw"
RAW_FILE_EXTENSIONS = [
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


class RawFinder:
    def __init__(self, path: str, raw_path: str, dest_path: str = "raw") -> None:
        self.path = pathlib.Path(path)
        self.raw_path = pathlib.Path(raw_path)
        self.dest_path = pathlib.Path(dest_path)

        self.files = self._get_files()

    def _get_files(self) -> list[pathlib.Path]:
        files = []
        for item in pathlib.Path(self.path).glob("*"):
            if item.is_file():
                files.append(item)
        return files

    @staticmethod
    def get_folder_name(file: pathlib.Path) -> str:
        return file.suffix.lower()[1:]

    def find(self) -> None:
        msg = (
            f"Find RAW files in {self.raw_path.resolve()} for {len(self.files)} files in {self.path.resolve()} "
            f"and copy them to {self.dest_path.resolve()}? [Y/n] "
        )
        try:
            if input(msg).lower() not in ["y", ""]:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            return

        self.dest_path.mkdir(exist_ok=True, parents=True)

        for file in self.files:
            if file.suffix:
                raw_file_found = False
                for raw_ext in RAW_FILE_EXTENSIONS:
                    raw_file = self.raw_path.joinpath(file.name.split(".")[0] + raw_ext)
                    if raw_file.exists():
                        print(f"RAW file {raw_file.name} found for {file.name}...")
                        self.dest_path.joinpath(raw_file.name).write_bytes(
                            raw_file.read_bytes()
                        )
                        raw_file_found = True

                if not raw_file_found:
                    print(f"No RAW file found for {file.name}!")

        print("Done")


def main():
    parser = argparse.ArgumentParser(
        prog="rawfinder", description="Find correspond raw files"
    )
    parser.add_argument(
        "jpeg", nargs="?", help="directory with jpeg files", default=os.getcwd()
    )
    parser.add_argument("raw", nargs="?", help="directory with source RAW files", default=os.getcwd())
    parser.add_argument(
        "-d",
        "--dst",
        help="destination dir",
        default=DEFAULT_DST_FOLDER,
        required=False,
    )
    args = parser.parse_args()
    print(args)

    RawFinder(args.jpeg, args.raw, args.dst).find()
