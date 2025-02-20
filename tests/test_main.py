import argparse
import logging
from pathlib import Path

import pytest


class TestMain:
    @pytest.mark.asyncio
    async def test_main_async(self, tmp_path: Path, mocker) -> None:
        jpeg_dir = tmp_path / "jpeg"
        raw_dir = tmp_path / "raw"
        dest_dir = tmp_path / "dest"
        jpeg_dir.mkdir()
        raw_dir.mkdir()
        dest_dir.mkdir()

        fake_args = argparse.Namespace(jpeg_dir=jpeg_dir, raw_dir=raw_dir, dest_dir=dest_dir)

        parse_args_patch = mocker.patch("rawfinder.main.parse_args", return_value=fake_args)
        test_logger = logging.getLogger("test")
        setup_logger_patch = mocker.patch("rawfinder.main.setup_logger", return_value=test_logger)

        app_mock = mocker.Mock()
        app_mock.run = mocker.AsyncMock()

        app_constructor_patch = mocker.patch("rawfinder.main.AsyncRawFinderApp", return_value=app_mock)

        from rawfinder.main import main_async

        await main_async()

        parse_args_patch.assert_called_once()
        setup_logger_patch.assert_called_once()
        app_constructor_patch.assert_called_once_with(jpeg_dir, raw_dir, dest_dir, test_logger)
        app_mock.run.assert_awaited_once()
