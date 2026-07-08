from rdkit import Chem
import os

def converter_mol_para_smiles(caminho_mol):
    """
    Converte um arquivo .mol em SMILES usando RDKit
    """
    if not os.path.exists(caminho_mol):
        print("Arquivo não encontrado:", caminho_mol)
        return None

    mol = Chem.MolFromMolFile(caminho_mol)

    if mol is None:
        print("Erro ao ler o arquivo MOL.")
        return None

    smiles = Chem.MolToSmiles(mol)
    return smiles


if __name__ == "__main__":
    arquivo_mol = "data/exemplo_molecula.mol"
    smiles = converter_mol_para_smiles(arquivo_mol)

    if smiles:
        print("✓ Conversão realizada com sucesso!")
        print("SMILES gerado:", smiles)
