import sqlite3
from pathlib import Path

from modules.configmgr import ConfigManager

class db:

    def __init__(self, DB_PATH: Path):
        super().__init__()
        self._conn = None
        self.DB_PATH = DB_PATH
        self.CACHE_DIR = Path.home() / ".cache" / "nix-search"

    def _init_db(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.DB_PATH)
        conn.executescript("""
            DROP TABLE IF EXISTS options;
            CREATE VIRTUAL TABLE options USING fts5(
                name,
                description,
                type,
                default_value,
                example,
                source,     == 'nixos', 'home-manager', 'nix-darwin'
                declarations,
                tokenize='porter unicode61'
            );
        """)
        conn.commit()
        return conn
