from __future__ import annotations

from typing import Dict, Any, Optional, Tuple
import sqlite3


def upsert_molecule(
    conn: sqlite3.Connection,
    *,
    mol_id: str,
    smiles_canonico: str,
    inchi: str,
    inchi_key: str
) -> int:
    """
    Insere molécula se não existir; se existir (mesmo InChIKey), retorna o id existente.
    """
    row = conn.execute(
        "SELECT id FROM molecules WHERE inchi_key = ?",
        (inchi_key,)
    ).fetchone()

    if row:
        return int(row["id"])

    cur = conn.execute(
        """
        INSERT INTO molecules (mol_id, smiles_canonico, inchi, inchi_key)
        VALUES (?, ?, ?, ?)
        """,
        (mol_id, smiles_canonico, inchi, inchi_key)
    )
    return int(cur.lastrowid)


def insert_properties(conn, *, molecule_id: int, run_id: str, props: Dict[str, Any]) -> int:
    cur = conn.execute(
        """
        INSERT INTO properties (
            run_id, molecule_id, molwt, logp, tpsa, hbd, hba, rotbonds, aromaticrings, formula
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            molecule_id,
            props.get("MolWt"),
            props.get("LogP"),
            props.get("TPSA"),
            props.get("HBD"),
            props.get("HBA"),
            props.get("RotBonds"),
            props.get("AromaticRings"),
            props.get("Formula"),
        )
    )
    return int(cur.lastrowid)

def create_run(conn, *, run_id: str, source: str = "api", notes: str = "") -> None:
    conn.execute(
        "INSERT OR IGNORE INTO runs (run_id, source, notes) VALUES (?, ?, ?)",
        (run_id, source, notes),
    )

def get_molecule_by_inchikey(conn: sqlite3.Connection, inchi_key: str) -> Optional[Dict[str, Any]]:
    row = conn.execute(
        "SELECT * FROM molecules WHERE inchi_key = ?",
        (inchi_key,)
    ).fetchone()

    if not row:
        return None
    return dict(row)


def get_properties_for_molecule(conn: sqlite3.Connection, molecule_id: int) -> list[Dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM properties WHERE molecule_id = ? ORDER BY id DESC",
        (molecule_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def insert_fingerprint(conn, molecule_id: int, fingerprint: str, nbits=2048, radius=2):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO fingerprints (molecule_id, fingerprint, nbits, radius)
        VALUES (?, ?, ?, ?)
        """,
        (molecule_id, fingerprint, nbits, radius),
    )

    return cursor.lastrowid

def get_all_fingerprints(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.fingerprint, m.inchi_key, m.smiles_canonico
        FROM fingerprints f
        JOIN molecules m ON f.molecule_id = m.id
    """)

    rows = cursor.fetchall()

    return [
        {
            "fingerprint": row[0],
            "inchi_key": row[1],
            "smiles": row[2],
        }
        for row in rows
    ]