import requests
import json

def testar_pubchem():
    cid = "2244"  # ibuprofeno
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight,IsomericSMILES/JSON"

    print(f"🔍 Testando PubChem para CID {cid}...")
    r = requests.get(url, timeout=10)
    dados = r.json()

    print(json.dumps(dados, indent=4))


def testar_chembl():
    chembl_id = "CHEMBL25"  # exemplo: Atenolol
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"

    print(f"🔍 Testando ChEMBL para {chembl_id}...")
    r = requests.get(url, timeout=10)

    print("Status HTTP:", r.status_code)
    print("Conteúdo recebido (primeiros 300 chars):")
    print(r.text[:300])  # para inspeção

    dados = r.json()  # agora funciona
    print(json.dumps(dados, indent=4))


if __name__ == "__main__":
    testar_pubchem()
    testar_chembl()
