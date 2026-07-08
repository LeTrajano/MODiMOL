from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity


def generate_fingerprint(smiles: str, radius: int = 2, nbits: int = 2048):
    """
    Gera fingerprint molecular (Morgan fingerprint).

    Parameters
    ----------
    smiles : str
        SMILES canônico
    radius : int
        raio do Morgan fingerprint
    nbits : int
        tamanho do vetor

    Returns
    -------
    RDKit ExplicitBitVect
    """

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        raise ValueError("SMILES inválido para geração de fingerprint")

    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nbits)

    return fp


def tanimoto_similarity(smiles1: str, smiles2: str):
    """
    Calcula similaridade molecular entre duas moléculas.
    """

    fp1 = generate_fingerprint(smiles1)
    fp2 = generate_fingerprint(smiles2)

    return TanimotoSimilarity(fp1, fp2)

from rdkit.DataStructs import BitVectToText


def fingerprint_to_string(fp):
    """
    Converte fingerprint RDKit em string para salvar no banco.
    """
    return BitVectToText(fp)

from rdkit.DataStructs import CreateFromBitString


def fingerprint_from_string(fp_str):
    return CreateFromBitString(fp_str)