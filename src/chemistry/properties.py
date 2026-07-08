# src/chemistry/properties.py
from __future__ import annotations

from typing import Dict, Any

from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors

from src.models import Molecule


def compute_properties(m: Molecule) -> Dict[str, Any]:
    """
    Calcula propriedades a partir de uma Molecule VALIDADA.
    Regra: NÃO faz parsing. NÃO chama MolFromSmiles.
    """
    mol = m.mol

    return {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Crippen.MolLogP(mol),
        "TPSA": rdMolDescriptors.CalcTPSA(mol),
        "HBD": Lipinski.NumHDonors(mol),
        "HBA": Lipinski.NumHAcceptors(mol),
        "RotBonds": Lipinski.NumRotatableBonds(mol),
        "AromaticRings": Lipinski.NumAromaticRings(mol),
        "Formula": rdMolDescriptors.CalcMolFormula(mol),
    }