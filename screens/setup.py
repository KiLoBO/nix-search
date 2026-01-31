from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Static,
)

from pathlib import Path

from modules.configmgr import ConfigManager
from modules.setupActions import SetupActions
from modules.generateDumps import generateDumps

from asyncio import sleep
from textual import work

welcome_text = """
Initial Setup
"""

sub_title = """
Click a button to run the action. Red lines MUST be run.
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
                yield Static(sub_title, id="sub-title")
                with Horizontal(classes="status-group"):
                    yield Static(
                        "Database created: ", id="db_exists", classes="status-line"
                    )
                    yield Button(
                        "Run Fix", id="db-button", classes="run-action", compact=True, variant="success"
                    )
                with Horizontal(classes="status-group"):
                    yield Static(
                        "NixOS Options dumped: ",
                        id="nixOpts_exists",
                        classes="status-line",
                    )
                    yield Button(
                        "Run Fix", id="nix-button", classes="run-action", compact=True, variant="success"
                    )
                with Horizontal(classes="status-group"):
                    yield Static(
                        "HM Options dumped: ", id="hmOpts_exists", classes="status-line"
                    )
                    yield Button(
                        "Run Fix", id="hm-button", classes="run-action", compact=True, variant="success"
                    )

    def on_mount(self) -> None:
        self.populate_checks(self.results)

    def populate_checks(self, results):
        for key, value in results.items():
            if key == "passed":
                continue

            color = "green" if value[1] else "red"
            text = self.query_one(f"#{key}", Static)
            text.update(f"[{color}]{value[0]}: {value[1]}[/]")

    def refresh_checks(self):
        results = self.checks.check_existing()
        self.populate_checks(results)

    @work
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        genDumps = generateDumps()
        cache_dir = Path(self.config.get("general.db_path"))
        button_id = event.button.id
        button = self.query_one(f"#{button_id}", Button)
        button.loading = True

        try:
            if button_id == "db-button":
                self.notify("Creating database...", severity="information")
                await self.test_loading()

            elif button_id == "nix-button":
                self.notify("Dumping NixOS options...", severity="information")
                await genDumps.genNixOptions(cache_dir.parent)

            elif button_id == "hm-button":
                self.notify("Dumping HM options...", severity="information")
                await genDumps.genHmOptions(cache_dir.parent)

        except Exception as e:
            self.notify(f"Error thrown. Will be printed to console. Error: {e}")
            print(f"Error with button process {button_id} -- Error: {e}")

        finally:
            self.refresh_checks()
            button.loading = False

    async def test_loading(self):
        await sleep(5)
        # button.loading = False
