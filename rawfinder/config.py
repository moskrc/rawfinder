import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import appdirs
import yaml
from pydantic import BaseModel, Field, field_validator

from rawfinder import raw_extensions
from rawfinder.exceptions import InvalidExceptionFormatError, MissingExtensionsError


class ReporterEnum(str, Enum):
    rich = "rich"
    plain = "plain"


@dataclass
class ConfigDefaults:
    verify_checksum: bool = True
    verify_checksum_chunk_size: int = 4 * 1024 * 1024
    reporter: ReporterEnum = ReporterEnum.plain
    dry_run: bool = False
    overwrite: bool = False
    extensions: dict[str, list[str]] = field(
        default_factory=lambda: {
            "photos": [".jpg", ".jpeg"],
            "sources": raw_extensions,
        }
    )


DEFAULTS = ConfigDefaults()


class AppConfig(BaseModel):
    verify_checksum_chunk_size: int = Field(
        default=DEFAULTS.verify_checksum_chunk_size,
        description=f"File verifier chunk size in bytes (default: {DEFAULTS.verify_checksum_chunk_size})",
        ge=1024,
    )
    reporter: ReporterEnum = Field(
        default=DEFAULTS.reporter,
        description=f"Progress reporter type ({[x.value for x in ReporterEnum]}): '{DEFAULTS.reporter}')",
    )
    dry_run: bool = Field(
        default=DEFAULTS.dry_run,
        description=f"Simulate operations without actual changes (default: {DEFAULTS.dry_run})",
    )
    verify_checksum: bool = Field(
        default=DEFAULTS.verify_checksum,
        description=f"Verify file integrity after copy (default: {DEFAULTS.verify_checksum})",
    )
    overwrite: bool = Field(
        default=DEFAULTS.overwrite, description=f"Overwrite existing files (default: {DEFAULTS.overwrite})"
    )
    extensions: dict[str, list[str]] = Field(
        default=DEFAULTS.extensions,
        description="File extensions for different file types (keys: 'photos', 'sources')",
    )

    @field_validator("extensions")
    @classmethod
    def validate_extensions(cls, v: dict[str, list[str]]) -> dict[str, list[str]]:
        required_keys = {"photos", "sources"}
        if not required_keys.issubset(v.keys()):
            missing = required_keys - set(v.keys())
            raise MissingExtensionsError(missing)

        for key, exts in v.items():
            for ext in exts:
                if not ext.startswith("."):
                    raise InvalidExceptionFormatError(ext, key, "Extension '{}' for '{}' must start with a dot (.)")
                if not ext[1:].isalnum():
                    raise InvalidExceptionFormatError(
                        ext, key, "Extension '{}' for '{}' must contain only alphanumeric characters after the dot"
                    )
        return v


class ConfigManager:
    @classmethod
    def get_user_config_path(cls) -> Path:
        config_dir = Path(appdirs.user_config_dir("rawfinder"))
        return config_dir / "config.yaml"

    @classmethod
    def get_default_config_path(cls) -> Path:
        return Path(__file__).parent / "data" / "default_config.yaml"


class ConfigLoader:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path

    def load(self) -> AppConfig:
        config_sources = [
            os.environ.get("RAWFINDER_CONFIG"),
            self.config_path,
            ConfigManager.get_user_config_path(),
        ]

        config_data: dict[str, Any] = {}
        for path in config_sources:
            if path and (cfg_path := Path(path)).exists():
                with cfg_path.open() as f:
                    config_data.update(yaml.safe_load(f) or {})
                break
        return AppConfig(**config_data)
