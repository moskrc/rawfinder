import hashlib
from pathlib import Path

from rawfinder.exceptions import ChecksumError


class FileIntegrityChecker:
    CHUNK_SIZE: int = 4_194_304

    def __init__(self, hash_algorithm: str = "sha256", chunk_size: int = CHUNK_SIZE):
        self.algorithm = hash_algorithm
        self.chunk_size = chunk_size

    def calculate_hash(self, file_path: Path) -> str:
        hash_func = hashlib.new(self.algorithm)
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def verify_copy(self, src: Path, dst: Path) -> None:
        src_hash = self.calculate_hash(src)
        dst_hash = self.calculate_hash(dst)

        if src_hash != dst_hash:
            raise ChecksumError(src, src_hash, dst, dst_hash)
