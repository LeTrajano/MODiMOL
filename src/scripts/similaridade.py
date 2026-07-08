import pandas as pd
from rdkit.Chem import DataStructs
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

from src.chemistry.validation import validate_smiles
from src.models import ValidationError

_MORGAN = GetMorganGenerator(radius=2, fpSize=2048)

def _fp_from_mol(mol):
    return _MORGAN.GetFingerprint(mol)

def calcular_similaridade(smiles_list, ref_smiles) -> pd.DataFrame:
    ref_v = validate_smiles(ref_smiles)
    if isinstance(ref_v, ValidationError):
        raise ValueError(f"SMILES de referência inválido: {ref_v.reason}")

    ref_fp = _fp_from_mol(ref_v.mol)

    resultados = []
    erros = []

    for smi in smiles_list:
        v = validate_smiles(smi)
        if isinstance(v, ValidationError):
            erros.append({"SMILES_input": str(smi), "reason": v.reason, "details": v.details or {}})
            continue

        fp = _fp_from_mol(v.mol)
        tanimoto = DataStructs.TanimotoSimilarity(ref_fp, fp)

        resultados.append({
            "SMILES_input": v.smiles_input,
            "SMILES": v.smiles,
            "InChIKey": v.inchi_key,
            "Tanimoto": tanimoto
        })

    df_out = pd.DataFrame(resultados).sort_values("Tanimoto", ascending=False)

    if erros:
        pd.DataFrame(erros).to_csv("outputs/erros_similaridade.csv", index=False)

    return df_out

if __name__ == "__main__":
    df = pd.read_csv("outputs/dataset_latest.csv")
    ref = df["SMILES"].iloc[0]

    saida = calcular_similaridade(df["SMILES"].tolist(), ref)
    saida.to_csv("outputs/similaridade_resultado.csv", index=False)

    print("✓ Similaridade calculada.")
    print("• Saída: outputs/similaridade_resultado.csv")
    print("• Erros (se houver): outputs/erros_similaridade.csv")