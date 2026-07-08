import os
import pandas as pd
from datetime import datetime

from src.chemistry.identificadores import gerar_id_local
from src.chemistry.validation import validate_smiles
from src.chemistry.properties import compute_properties
from src.models import ValidationError

from src.persistence.database import get_connection, init_db
from src.persistence.repository import upsert_molecule, insert_properties


def pipeline(
    csv_entrada="data/propriedades_pipeline.csv",
    csv_saida="data/propriedades_avancadas.csv",
    csv_erros="data/erros_validacao.csv",
):
    df = pd.read_csv(csv_entrada)

    validos = []
    erros = []

    # ✅ run_id único por execução (histórico)
    run_id = datetime.now().strftime("RUN_%Y%m%d_%H%M%S")

    print("\n=== PIPELINE BÁSICO — VALIDAÇÃO + PROPRIEDADES (CORE) ===")
    print("Run ID:", run_id)

    for idx, smi in enumerate(df["SMILES"]):
        mol_id = gerar_id_local(idx)

        v = validate_smiles(smi)

        if isinstance(v, ValidationError):
            erros.append({
                "mol_id": mol_id,
                "SMILES_input": str(smi),
                "reason": v.reason,
                "details": (v.details or {}),
            })
            continue

        props = compute_properties(v)

        validos.append({
            "run_id": run_id,                 # ✅ adiciona no dataframe também
            "mol_id": mol_id,
            "SMILES_input": v.smiles_input,
            "SMILES": v.smiles,               # canônico
            "InChI": v.inchi,
            "InChIKey": v.inchi_key,

            "MolWt": props["MolWt"],
            "LogP": props["LogP"],
            "TPSA": props["TPSA"],
            "HBD": props["HBD"],
            "HBA": props["HBA"],
            "RotBonds": props["RotBonds"],
            "AromaticRings": props["AromaticRings"],
            "Formula": props["Formula"],
        })

    # ---------------------------
    # Salvar CSV
    # ---------------------------
    os.makedirs("data", exist_ok=True)
    df_out = pd.DataFrame(validos)
    df_out.to_csv(csv_saida, index=False)

    # ---------------------------
    # Persistência SQLite (histórico por run_id)
    # ---------------------------
    init_db()
    conn = get_connection()

    try:
        for row in validos:
            mol_db_id = upsert_molecule(
                conn,
                mol_id=row["mol_id"],
                smiles_canonico=row["SMILES"],
                inchi=row["InChI"],
                inchi_key=row["InChIKey"],
            )

            # ✅ grava histórico: uma linha de properties por molécula POR execução
            insert_properties(
                conn,
                molecule_id=mol_db_id,
                run_id=run_id,
                props=row
            )

        conn.commit()
        print("✓ Dados inseridos no SQLite:", "data/projeto_molecular.db")

    finally:
        conn.close()

    # ---------------------------
    # Salvar erros
    # ---------------------------
    if erros:
        df_err = pd.DataFrame(erros)
        df_err.to_csv(csv_erros, index=False)
        print(f"⚠ Alguns SMILES falharam. Erros salvos em: {csv_erros}")

    print("✓ Pipeline concluído!")
    print("Arquivo gerado:", csv_saida)

    return df_out


if __name__ == "__main__":
    pipeline()