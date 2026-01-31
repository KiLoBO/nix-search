from pathlib import Path

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    Header,
    Static,
)

from modules.configmgr import ConfigManager
from modules.setupActions import SetupActions
from modules.db import db
from modules.generateDumps import generateDumps
from screens.setup import SetupScreen


class NixSearch(App):
    def __init__(self):
        super().__init__()
        config_path = Path.home() / ".config" / "nix-search" / "config.yml"
        self.config = ConfigManager(config_path)
        self.checks = SetupActions(self.config)
        self.db_path = self.config.get("general.db_path")
        # opts_db = db(self.db_path)
        # opts_db._init_db()
        self.cache_dir = Path(self.db_path).parent

    def on_mount(self):
        if self.config.get("general.theme"):
            self.theme = self.config.get("general.theme")
        else:
            self.theme = "dracula"

        results = self.checks.check_existing()
        if not results["passed"]:
            self.push_screen(SetupScreen(self.config, results))
        # self.gen_dumps()

    @work(exclusive=True)
    async def gen_dumps(self):
        self.notify("Dumping Nix Options")
        genDumps = generateDumps()
        await genDumps.genNixOptions(self.cache_dir)
        self.notify("Finished dumping Nix Options")

        self.notify("Dumping HM options")
        await genDumps.genHmOptions(self.cache_dir)
        self.notify("Finished dumping HM options")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="textDisplay")
        yield Footer()


if __name__ == "__main__":
    app = NixSearch()
    app.run()
