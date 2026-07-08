# src/chemistry/validation.py
from __future__ import annotations

from dataclasses import asdict
from typing import Tuple, Union, Optional

from rdkit import Chem

from src.models import Molecule, ValidationError


def validate_smiles(
    smiles_input: str,
    *,
    sanitize: bool = True,
    canonical: bool = True
) -> Union[Molecule, ValidationError]:
    """
    Valida e normaliza um SMILES.
    REGRA: este é o ÚNICO lugar do projeto onde Chem.MolFromSmiles() deve existir.

    Retorna:
      - Molecule (sucesso)
      - ValidationError (falha)
    """
    if smiles_input is None or str(smiles_input).strip() == "":
        return ValidationError(input_value=str(smiles_input), reason="empty_input")

    smiles_input = str(smiles_input).strip()

    try:
        mol = Chem.MolFromSmiles(smiles_input)
        if mol is None:
            return ValidationError(input_value=smiles_input, reason="invalid_smiles")

        if sanitize:
            # Sanitização RDKit (valência, aromaticidade, etc.)
            Chem.SanitizeMol(mol)

        smiles_canonico = Chem.MolToSmiles(mol, canonical=canonical)

        # Identidade estrutural
        inchi = Chem.MolToInchi(mol)
        inchi_key = Chem.InchiToInchiKey(inchi)

        return Molecule(
            smiles=smiles_canonico,
            inchi=inchi,
            inchi_key=inchi_key,
            mol=mol,
            smiles_input=smiles_input
        )

    except Exception as e:
        return ValidationError(
            input_value=smiles_input,
            reason="rdkit_exception",
            details={"error": str(e)}
        )