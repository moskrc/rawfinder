import pytest

from rawfinder.config import DEFAULTS, AppConfig, ConfigLoader, ConfigManager


class AppConfigTest:
    def test_default_values(self):
        config = AppConfig()
        assert config.verify_checksum_chunk_size == DEFAULTS.verify_checksum_chunk_size
        assert config.reporter == DEFAULTS.reporter
        assert config.dry_run == DEFAULTS.dry_run

    def test_custom_values(self):
        custom_extensions = {"photos": [".png"], "sources": [".cr2"]}
        config = AppConfig(extensions=custom_extensions)
        assert config.extensions == custom_extensions

    def test_missing_extension_keys(self):
        with pytest.raises(ValueError, match="Missing extensions for: {'photos'}"):
            AppConfig(extensions={"sources": [".cr2"]})


class ConfigManagerTest:
    def test_get_user_config_path(self):
        path = ConfigManager.get_user_config_path()
        assert path.name == "config.yaml"

    def test_get_default_config_path(self):
        path = ConfigManager.get_default_config_path()
        assert path.name == "default_config.yaml"


class TestConfigLoader:
    def test_load_from_env_var(self, monkeypatch, config_file):
        monkeypatch.setenv("RAWFINDER_CONFIG", str(config_file))
        loader = ConfigLoader()
        config = loader.load()
        assert config.verify_checksum_chunk_size == 8192

    def test_load_from_custom_path(self, config_file):
        loader = ConfigLoader(config_path=config_file)
        config = loader.load()
        assert config.dry_run is False

    def test_load_from_user_config(self, monkeypatch, tmp_path):
        user_config = tmp_path / "config.yaml"
        user_config.parent.mkdir(parents=True, exist_ok=True)
        user_config.write_text("overwrite: true")
        monkeypatch.setattr("appdirs.user_config_dir", lambda _: str(tmp_path))

        loader = ConfigLoader()
        config = loader.load()
        assert config.overwrite is True

    def test_no_config_found(self):
        loader = ConfigLoader()
        config = loader.load()
        assert config.verify_checksum_chunk_size == DEFAULTS.verify_checksum_chunk_size
