import json
import sqlite3
from pathlib import Path
from typing import Optional

class Database:
    def __init__(self, db_path: Path):
        super().__init__()
        self._conn: Optional[sqlite3.Connection] = None
        self.db_path = db_path
        self.cache_dir = self.db_path.parent

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            if not self.db_path.exists():
                raise FileNotFoundError(f"Database not found at {self.db_path}. Run Setup First")
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            DROP TABLE IF EXISTS options;
            DROP TABLE IF EXISTS packages;

            CREATE VIRTUAL TABLE options USING fts5(
                name,
                description,
                type,
                default_value,
                example,
                source,
                declarations,
                tokenize='porter unicode61'
            );

            CREATE VIRTUAL TABLE packages USING fts5(
                attribute,
                pname,
                version,
                description,
                homepage,
                license,
                tokenize='porter unicode61'
            );
        """)
        conn.commit()
        return conn

    def ingest_options(self, conn: sqlite3.Connection, json_path: Path, source: str) -> int:
        with open(json_path) as f:
            options = json.load(f)

        rows = []
        for name, opt in options.items():
            rows.append((
                name,
                opt.get("description", ""),
                opt.get("type", ""),
                json.dumps(opt.get("default", "")),
                json.dumps(opt.get("example", "")),
                source,
                json.dumps(opt.get("declarations", [])),
            ))

        conn.executemany(
            "INSERT INTO options(name, description, type, default_value, example, source, declarations) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
        return len(rows)

    def ingest_packages(self, conn: sqlite3.Connection, json_path: Path, system: str = "x86_64-linux") -> int:
        with open(json_path) as f:
            data = json.load(f)

        if "packages" in data:
            packages = data["packages"].get(system, {})
        else:
            packages = {k.removeprefix("nixpkgs."): v for k, v in data.items()}

        rows = []
        for attr, pkg in packages.items():
            meta = pkg.get("meta", {})
            homepage = meta.get("homepage", "")
            if not isinstance(homepage, str):
                homepage = ""

            rows.append((
                attr,
                pkg.get("pname", ""),
                pkg.get("version", ""),
                meta.get("description", ""),
                homepage,
            ))

        conn.executemany(
            "INSERT INTO packages(attribute, pname, version, description, homepage) "
            "VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
        return len(rows)

    def search_options(self, query: str, source: Optional[str] = None, limit: int = 50) -> list[dict]:
        if source:
            results = self.conn.execute(
                """
                SELECT name, description, type, default_value, example, source, declarations
                FROM options
                WHERE options MATCH ? AND source = ?
                ORDER by rank
                LIMIT ?
                """,
                (query, source, limit),
            ).fetchall()

        else:
            results = self.conn.execute(
                """
                SELECT name, description, type, default_value, example, source, declarations
                FROM options
                WHERE options MATCH ?
                ORDER by rank
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()

        return [dict(r) for r in results]

    def search_packages(self, query: str, limit: int = 50) -> list[dict]:
        results = self.conn.execute(
            """
            SELECT attribute, pname, version, description, homepage
            FROM packages
            WHERE packages MATCH ?
            ORDER by rank
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()

        return [dict(r) for r in results]

    def search_all(self, query: str, limit: int = 50) -> dict[str, list[dict]]:
        return {
            "options": self.search_options(query, limit=limit),
            "packages": self.search_packages(query, limit=limit),
        }
