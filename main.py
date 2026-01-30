from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    Header,
)

from pathlib import Path
from modules.configmgr import ConfigManager
from modules.db import db

class NixSearch(App):
    def __init__(self):
        config_path = Path.home() / ".config" / "nix-search" / "config.yml"
        self.config = ConfigManager(config_path)
        self.db_path = Path(self.config.get("general.db_path"))
        db.init_db()

    def on_mount(self):
        if self.config.get("general.theme"):
            self.theme = self.config.get("general.theme")
        else:
            self.theme = "dracula"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()


if __name__ == "__main__":
    app = NixSearch()
    app.run()
