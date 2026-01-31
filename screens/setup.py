from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Static,
)

from modules.configmgr import ConfigManager
from modules.setupActions import SetupActions

welcome_text = """
    WELCOME, YOU NEED TO DO SETUP
"""


class SetupScreen(Screen):
    CSS_PATH = "../css/setup.tcss"

    def __init__(self, config_manager: ConfigManager, results):
        super().__init__()
        self.results: dict = results
        self.config = config_manager
        self.checks = SetupActions(self.config)

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="main-vert"):
                yield Static(welcome_text, id="title")
                with Horizontal(classes="status-group"):
                    yield Static(
                        "Database created: ", id="db_exists", classes="status-line"
                    )
                    yield Button(
                        "Run Fix", id="db-button", classes="run-action", compact=True
                    )
                with Horizontal(classes="status-group"):
                    yield Static(
                        "NixOS Options dumped: ",
                        id="nixOpts_exists",
                        classes="status-line",
                    )
                    yield Button(
                        "Run Fix", id="nix-button", classes="run-action", compact=True
                    )
                with Horizontal(classes="status-group"):
                    yield Static(
                        "HM Options dumped: ", id="hmOpts_exists", classes="status-line"
                    )
                    yield Button(
                        "Run Fix", id="hm-button", classes="run-action", compact=True
                    )

    def on_mount(self) -> None:
        for key, value in self.results.items():
            if key == "passed":
                continue

            color = "green" if value[1] else "red"
            text = self.query_one(f"#{key}", Static)
            text.update(f"[{color}]{value[0]}: {value[1]}[/]")
