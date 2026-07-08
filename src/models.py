from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class Molecule:
    """
    Objeto canônico interno do sistema.
    Representa uma molécula VALIDADA pelo RDKit.

    - smiles: SMILES canônico (fonte da verdade textual)
    - inchi/inchi_key: identidade estrutural global
    - mol: objeto RDKit (mantido aqui para evitar reparse)
    - smiles_input: opcional, para rastreabilidade do que entrou
    """
    smiles: str
    inchi: str
    inchi_key: str
    mol: Any
    smiles_input: Optional[str] = None


@dataclass(frozen=True)
class ValidationError:
    """
    Erro padronizado de validação/normalização.
    Útil para retornar status sem quebrar pipelines.
    """
    input_value: str
    reason: str
    details: Optional[Dict[str, Any]] = None