import logging
from pathlib import Path

import pytest

from rawfinder.app import AsyncRawFinderApp


class TestAsyncRawFinderApp:
    @pytest.mark.asyncio
    async def test_run_executes_copy(self, tmp_path: Path, mocker) -> None:
        jpeg_dir = tmp_path / "jpeg"
        raw_dir = tmp_path / "raw"
        dest_dir = tmp_path / "dest"
        jpeg_dir.mkdir()
        raw_dir.mkdir()
        dest_dir.mkdir()

        jpeg_file = jpeg_dir / "sample.jpg"
        jpeg_file.write_text("dummy jpeg content")

        raw_file = raw_dir / "sample.raw"
        raw_content = b"dummy raw content"
        raw_file.write_bytes(raw_content)  # type: ignore[arg-type]

        mocker.patch("builtins.input", return_value="y")

        test_logger = logging.getLogger("test")
        test_logger.setLevel(logging.DEBUG)

        app = AsyncRawFinderApp(jpeg_dir, raw_dir, dest_dir, test_logger)
        await app.run()

        dest_file = dest_dir / raw_file.name
        assert dest_file.exists(), "Destination RAW file should exist after copying."
        assert dest_file.read_bytes() == raw_content, "Content of the copied file should match the source RAW file."

    @pytest.mark.asyncio
    async def test_run_cancelled(self, tmp_path: Path, mocker) -> None:
        jpeg_dir = tmp_path / "jpeg"
        raw_dir = tmp_path / "raw"
        dest_dir = tmp_path / "dest"
        jpeg_dir.mkdir()
        raw_dir.mkdir()
        dest_dir.mkdir()

        jpeg_file = jpeg_dir / "sample.jpg"
        jpeg_file.write_text("dummy jpeg content")
        raw_file = raw_dir / "sample.raw"
        raw_content = b"dummy raw content"
        raw_file.write_bytes(raw_content)  # type: ignore[arg-type]

        mocker.patch("builtins.input", return_value="n")

        test_logger = logging.getLogger("test")
        test_logger.setLevel(logging.DEBUG)

        app = AsyncRawFinderApp(jpeg_dir, raw_dir, dest_dir, test_logger)
        await app.run()

        dest_file = dest_dir / raw_file.name
        assert not dest_file.exists(), "Destination RAW file should not exist when copying is cancelled."
