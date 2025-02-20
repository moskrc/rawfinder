from pathlib import Path

import pytest

from rawfinder.copier import AsyncFileCopier


class TestAsyncFileCopier:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "filename,content",
        [
            ("sample.txt", b"Test content for AsyncFileCopier."),
            ("empty.txt", b""),
        ],
    )
    async def test_copy_files(self, tmp_path: Path, copier: AsyncFileCopier, filename: str, content: bytes):
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        src_file = src_dir / filename
        src_file.write_bytes(content)  # type: ignore[arg-type]

        dest_dir = tmp_path / "dest"
        await copier.copy(src_file, dest_dir)

        dest_file = dest_dir / filename
        assert dest_file.exists(), "Destination file should exist."
        assert dest_file.read_bytes() == content, "Copied file content should match the source file content."

    @pytest.mark.asyncio
    async def test_copy_file_multiple_chunks(self, mocker, tmp_path: Path, copier: AsyncFileCopier) -> None:
        mocker.patch.object(AsyncFileCopier, "CHUNK_SIZE", 3)

        src_dir = tmp_path / "src_multi"
        src_dir.mkdir()
        src_file = src_dir / "multi.txt"
        content = b"0123456789ABCDEF"
        src_file.write_bytes(content)  # type: ignore[arg-type]

        dest_dir = tmp_path / "dest_multi"
        await copier.copy(src_file, dest_dir)

        dest_file = dest_dir / src_file.name
        assert dest_file.exists(), "Destination file should exist."
        assert dest_file.read_bytes() == content, "Copied file content should match the source across multiple chunks."
