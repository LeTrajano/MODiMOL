from src.chemistry.fingerprints import (
    generate_fingerprint,
    fingerprint_from_string
)
from rdkit.DataStructs import TanimotoSimilarity

from src.persistence.repository import get_all_fingerprints
from src.persistence.database import get_connection


def search_similar(smiles: str, top_k: int = 5):

    conn = get_connection()

    try:
        db_data = get_all_fingerprints(conn)
    finally:
        conn.close()

    query_fp = generate_fingerprint(smiles)

    results = []

    for item in db_data:
        db_fp = fingerprint_from_string(item["fingerprint"])

        score = TanimotoSimilarity(query_fp, db_fp)

        results.append({
            "inchi_key": item["inchi_key"],
            "smiles": item["smiles"],
            "similarity": score
        })

    # ordenar por similaridade
    results_sorted = sorted(
        results,
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results_sorted[:top_k]