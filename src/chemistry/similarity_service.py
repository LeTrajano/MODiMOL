from src.chemistry.fingerprints import tanimoto_similarity


def compute_similarity(smiles_a: str, smiles_b: str):

    score = tanimoto_similarity(smiles_a, smiles_b)

    return {
        "smiles_a": smiles_a,
        "smiles_b": smiles_b,
        "similarity": score
    }