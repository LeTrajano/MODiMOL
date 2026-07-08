from typing import Dict, Any, Union

from src.chemistry.validation import validate_smiles
from src.chemistry.properties import compute_properties
from src.models import ValidationError


def normalize_structure(smiles: str) -> Union[Dict[str, Any], ValidationError]:
    """
    Normaliza uma estrutura molecular a partir de um SMILES.

    Pipeline:
    SMILES → validação RDKit → canonicalização → InChI → InChIKey → propriedades
    """

    v = validate_smiles(smiles)

    if isinstance(v, ValidationError):
        return v

    props = compute_properties(v)

    return {
        "smiles_input": v.smiles_input,
        "smiles_canonico": v.smiles,
        "inchi": v.inchi,
        "inchi_key": v.inchi_key,
        "properties": props,
    }