from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional


DEFAULT_DB_PATH = Path("data/projeto_molecular.db")
SCHEMA_PATH = Path("src/persistence/schema.sql")


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Cria conexão SQLite com foreign keys ligadas.
    """
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row

    # IMPORTANTÍSSIMO no SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """
    Inicializa banco criando as tabelas.
    """
    conn = get_connection(db_path)
    try:
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Schema não encontrado: {SCHEMA_PATH}")

        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
        