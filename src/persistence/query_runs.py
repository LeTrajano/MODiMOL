from __future__ import annotations

import argparse
import sqlite3
import pandas as pd

from src.persistence.database import get_connection


def list_runs(conn: sqlite3.Connection, limit: int = 20) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT run_id, COUNT(*) as n_props, MIN(created_at) as started_at, MAX(created_at) as finished_at
        FROM properties
        GROUP BY run_id
        ORDER BY finished_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def dataset_for_run(conn: sqlite3.Connection, run_id: str) -> pd.DataFrame:
    rows = conn.execute("""
        SELECT
            m.mol_id,
            m.smiles_canonico as SMILES,
            m.inchi as InChI,
            m.inchi_key as InChIKey,
            p.run_id,
            p.created_at,
            p.molwt as MolWt,
            p.logp as LogP,
            p.tpsa as TPSA,
            p.hbd as HBD,
            p.hba as HBA,
            p.rotbonds as RotBonds,
            p.aromaticrings as AromaticRings,
            p.formula as Formula
        FROM properties p
        JOIN molecule m ON m.id = p.molecule_id
        WHERE p.run_id = ?
        ORDER BY m.mol_id ASC
    """, (run_id,)).fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def latest_dataset(conn: sqlite3.Connection) -> pd.DataFrame:
    # pega o último run_id (mais recente por finished_at)
    run = conn.execute("""
        SELECT run_id
        FROM properties
        GROUP BY run_id
        ORDER BY MAX(created_at) DESC
        LIMIT 1
    """).fetchone()

    if not run:
        return pd.DataFrame()

    return dataset_for_run(conn, run["run_id"])


def main():
    parser = argparse.ArgumentParser(description="Consultas de runs e datasets no SQLite.")
    parser.add_argument("--list", action="store_true", help="Listar runs disponíveis")
    parser.add_argument("--run_id", default=None, help="Extrair dataset de um run específico")
    parser.add_argument("--latest", action="store_true", help="Extrair dataset do run mais recente")
    parser.add_argument("--out", default=None, help="Salvar dataset em CSV (opcional)")
    args = parser.parse_args()

    conn = get_connection()
    try:
        if args.list:
            df = list_runs(conn)
            print(df.to_string(index=False))
            return

        if args.run_id:
            df = dataset_for_run(conn, args.run_id)
        elif args.latest:
            df = latest_dataset(conn)
        else:
            print("Use --list, --run_id ou --latest.")
            return

        if df.empty:
            print("⚠ Nenhum dado encontrado.")
            return

        if args.out:
            df.to_csv(args.out, index=False)
            print(f"✓ Dataset salvo em: {args.out}")
        else:
            print(df.head(10).to_string(index=False))
            print(f"\nLinhas: {len(df)}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()