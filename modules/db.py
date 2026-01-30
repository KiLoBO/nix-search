import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".cache" / "nix-search" / "options.db"

class db:
