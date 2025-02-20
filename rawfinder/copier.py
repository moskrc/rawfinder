import asyncio
from pathlib import Path

import aiofiles


class AsyncFileCopier:
    CHUNK_SIZE: int = 16 * 1024 * 1024  # 16 MB
    DEFAULT_SEMAPHORE_LIMIT: int = 5

    def __init__(self, semaphore: asyncio.Semaphore | None = None):
        self.semaphore = semaphore or asyncio.Semaphore(self.DEFAULT_SEMAPHORE_LIMIT)

    async def copy(self, src: Path, dest_dir: Path) -> None:
        """
        Copy file from src to dest_dir. Create dest_dir if not exists.
        :param src:
        :param dest_dir:
        :return:
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        async with self.semaphore, aiofiles.open(src, "rb") as sf, aiofiles.open(dest, "wb") as df:
            while chunk := await sf.read(self.CHUNK_SIZE):
                await df.write(chunk)
