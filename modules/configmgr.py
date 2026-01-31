from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG = {
    "general": {
        "theme": "dracula",
        "nixpkgs_version": "25.11",
        "db_path": str(Path.home() / ".cache" / "nix-search" / "options.db"),
    }
}


class ConfigManager:
    def __init__(self, config_path: str | Path) -> None:
        super().__init__()
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            self._create_default_config()

        try:
            with self.config_path.open("r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                return config if config else {}
        except Exception as e:
            print(f"Error opening config: {e}")
            return DEFAULT_CONFIG.copy()

    def _create_default_config(self) -> None:
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open("w", encoding="utf-8") as file:
                yaml.safe_dump(DEFAULT_CONFIG, file, default_flow_style=False)
        except Exception as e:
            print(f"Could not create default config: {e}")

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split(".")
        value = self.config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def reload(self) -> None:
        self.config = self._load_config()
