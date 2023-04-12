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

IMAGE_FILE_EXTENSIONS = [".jpeg", ".jpg"]


class RawFinder:
    def __init__(self, path: str, raw_path: str, dest_path: str = None) -> None:
        self.image_path = pathlib.Path(path)
        self.raw_path = pathlib.Path(raw_path)

        if not dest_path:
            self.dest_path = self.image_path / DEFAULT_DST_FOLDER
        else:
            self.dest_path = pathlib.Path(dest_path)

        self.image_files = self._get_image_files(self.image_path, IMAGE_FILE_EXTENSIONS)

        self.raw_files = self._get_image_files(
            self.raw_path, RAW_FILE_EXTENSIONS, recursively=True
        )

    def _get_image_files(
        self, folder: pathlib.Path, extensions: list[str], recursively: bool = False
    ) -> list[pathlib.Path]:
        return [
            item
            for item in pathlib.Path(folder).glob("**/*" if recursively else "*")
            if item.is_file() and item.suffix.lower() in extensions
        ]

    def prompt(self):
        msg = (
            f"# Images: '{self.image_path}' ({len(self.image_files)} image files)\n"
            f"# RAWs: '{self.raw_path}' ({len(self.raw_files)} raw files)\n"
            f"# Find corresponding RAW files and copy them to '{self.dest_path}'? [Y/n] "
        )

        if input(msg).lower() not in ["y", ""]:
            raise KeyboardInterrupt

    def get_corresponding_raw(self, image_file):
        image_name = image_file.stem.lower()
        raw_set = set(self.raw_files)
        for raw_file in raw_set:
            if raw_file.stem.lower() == image_name:
                return raw_file

    def find(self) -> None:
        try:
            self.prompt()
        except KeyboardInterrupt:
            return

        self.dest_path.mkdir(exist_ok=True, parents=True)

        for file in self.image_files:
            if raw_file := self.get_corresponding_raw(file):
                copy_path = self.dest_path / raw_file.name
                print(
                    f"RAW file {raw_file.name} found for {file.name}, copy to {copy_path}..."
                )
                copy_path.write_bytes(raw_file.read_bytes())
            else:
                print(f"No RAW file found for {file.name}!")

        print("Done")


def main():
    parser = argparse.ArgumentParser(
        prog="rawfinder", description="Find corresponding raw files for images"
    )
    parser.add_argument(
        "image_dir", nargs="?", help="directory with images", default=os.getcwd()
    )
    parser.add_argument(
        "raw_dir", nargs="?", help="directory with RAW files", default=os.getcwd()
    )
    parser.add_argument(
        "-t",
        "--target",
        help="destination dir",
        required=False,
    )
    args = parser.parse_args()

    RawFinder(args.image_dir, args.raw_dir, args.target).find()


if __name__ == "__main__":
    main()
