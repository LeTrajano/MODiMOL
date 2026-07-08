# src/scripts/clustering.py
import os
import pandas as pd
from sklearn.cluster import KMeans

from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

from src.chemistry.validation import validate_smiles
from src.models import ValidationError


_MORGAN = GetMorganGenerator(radius=2, fpSize=2048)


def _fp_from_mol(mol):
    return _MORGAN.GetFingerprint(mol)


def gerar_clustering(
    df: pd.DataFrame,
    *,
    smiles_col="SMILES",
    n_clusters=3,
    random_state=42,
    out_csv="outputs/clustering_resultado.csv",
    err_csv="outputs/erros_clustering.csv",
) -> pd.DataFrame:
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    valid_rows = []
    X = []
    erros = []

    for _, row in df.iterrows():
        smi = row[smiles_col]
        v = validate_smiles(smi)

        if isinstance(v, ValidationError):
            erros.append({
                "SMILES_input": str(smi),
                "reason": v.reason,
                "details": v.details or {}
            })
            continue

        fp = _fp_from_mol(v.mol)

        r = row.to_dict()
        r["SMILES_input"] = v.smiles_input
        r["SMILES"] = v.smiles
        r["InChIKey"] = v.inchi_key

        valid_rows.append(r)
        X.append(list(fp))  # KMeans precisa matriz numérica

    if not valid_rows:
        raise ValueError("Nenhuma molécula válida para clustering.")

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    labels = kmeans.fit_predict(X)

    df_out = pd.DataFrame(valid_rows)
    df_out["Cluster"] = labels

    df_out.to_csv(out_csv, index=False)

    if erros:
        pd.DataFrame(erros).to_csv(err_csv, index=False)

    return df_out


if __name__ == "__main__":
    print("▶ Iniciando clustering...")

    df = pd.read_csv("outputs/dataset_latest.csv")
    out = gerar_clustering(df, n_clusters=3)

    print("✓ Clustering concluído.")
    print("• Linhas válidas:", len(out))
    print("• Saída:", "outputs/clustering_resultado.csv")
    print("• Erros (se houver):", "outputs/erros_clustering.csv")