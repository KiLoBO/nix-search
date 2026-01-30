from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Static,
)

from modules.configmgr import ConfigManager

welcome_text = """
    WELCOME, YOU NEED TO DO SETUP
"""


class SetupScreen(Screen):
    CSS_PATH = "../css/setup.tcss"

    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager

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
        self.check_existing_files()

    def check_existing_files(self):
        db_path = Path(self.config.get("general.db_path"))
        nixOpts = db_path.parent / "NixOS_options.json"
        hmOpts = db_path.parent / "Home-Manager_options.json"

        if db_path.exists():
            color = "green"
            self.query_one("#db_exists", Static).update(
                f"[{color}]Database created: {db_path.exists()}[/]"
            )
        else:
            color = "red"
            self.query_one("#db_exists", Static).update(
                f"[{color}]Database created: {db_path.exists()}[/]"
            )

        if nixOpts.exists():
            color = "green"
            self.query_one("#nixOpts_exists", Static).update(
                f"[{color}]NixOS Options dumped: {nixOpts.exists()}[/]"
            )
        else:
            color = "red"
            self.query_one("#nixOpts_exists", Static).update(
                f"[{color}]NixOS Options dumped: {nixOpts.exists()}[/]"
            )

        if hmOpts.exists():
            color = "green"
            self.query_one("#hmOpts_exists", Static).update(
                f"[{color}]HM Options dumped: {hmOpts.exists()}[/]"
            )
        else:
            color = "red"
            self.query_one("#hmOpts_exists", Static).update(
                f"[{color}]HM Options dumped: {hmOpts.exists()}[/]"
            )
