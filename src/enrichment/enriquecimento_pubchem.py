import requests
import pandas as pd

def enrich_pubchem(df):
    enriched = []

    for smi in df["SMILES"]:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smi}/property/XLogP,HBondDonorCount,HBondAcceptorCount/JSON"
        try:
            r = requests.get(url).json()
            props = r["PropertyTable"]["Properties"][0]
            props["SMILES"] = smi
            enriched.append(props)
        except:
            pass

    new_df = pd.DataFrame(enriched)
    new_df.to_csv("data/propriedades_enriquecidas.csv", index=False)
    return new_df


if __name__ == "__main__":
    base = pd.read_csv("data/propriedades_pipeline.csv")
    enriched = enrich_pubchem(base)
    print(enriched)
