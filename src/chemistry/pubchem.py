import requests


def get_iupac_name(smiles):

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
        f"compound/smiles/{smiles}/property/IUPACName/JSON"
    )

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        return (
            data["PropertyTable"]["Properties"][0]["IUPACName"]
        )

    except Exception:
        return None