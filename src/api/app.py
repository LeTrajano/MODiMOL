from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from rdkit import Chem
from rdkit.Chem import Draw

import io

from src.chemistry.validation import validate_smiles
from src.chemistry.properties import compute_properties
from src.models import ValidationError

from src.chemistry.fingerprints import generate_fingerprint, fingerprint_to_string
from src.chemistry.similarity_service import compute_similarity
from src.chemistry.search_service import search_similar
from src.chemistry.pubchem import get_iupac_name

from src.persistence.database import init_db, get_connection
from src.persistence.repository import (
    upsert_molecule,
    insert_properties,
    get_molecule_by_inchikey,
    get_properties_for_molecule,
    create_run,
    insert_fingerprint,
)

# -----------------------------
# APP
# -----------------------------
app = FastAPI(
    title="MODiMOL – API Molecular",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# inicializa banco
init_db()

# -----------------------------
# MODELS
# -----------------------------
class NormalizeRequest(BaseModel):
    smiles: str
    mol_id: Optional[str] = None
    save: bool = True
    run_id: Optional[str] = None


class NormalizeResponse(BaseModel):

    ok: bool
    smiles_canonico: Optional[str] = None
    inchi: Optional[str] = None
    inchi_key: Optional[str] = None
    iupac_name: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    db_molecule_id: Optional[int] = None
    error: Optional[Dict[str, Any]] = None

class SimilarityRequest(BaseModel):
    smiles_a: str
    smiles_b: str


class SearchRequest(BaseModel):
    smiles: str
    top_k: int = 5


# -----------------------------
# HEALTH
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "MODiMOL API rodando"}


# -----------------------------
# IMAGEM 
# -----------------------------
@app.get("/molecules/image/{smiles}")
def get_molecule_image(smiles: str):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        raise HTTPException(status_code=400, detail="SMILES inválido")

    img = Draw.MolToImage(mol)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


# -----------------------------
# NORMALIZAÇÃO
# -----------------------------
@app.post("/molecules/normalize", response_model=NormalizeResponse)
def normalize(req: NormalizeRequest):

    v = validate_smiles(req.smiles)

    if isinstance(v, ValidationError):
        return NormalizeResponse(
            ok=False,
            error={
                "reason": v.reason,
                "input": v.input_value,
            },
        )

    props = compute_properties(v)

    iupac_name = get_iupac_name(v.smiles)

    fp = generate_fingerprint(v.smiles)
    fp_str = fingerprint_to_string(fp)

    db_id = None

    if req.save:
        conn = get_connection()

        try:
            db_id = upsert_molecule(
                conn,
                mol_id=req.mol_id or "MOL_API",
                smiles_canonico=v.smiles,
                inchi=v.inchi,
                inchi_key=v.inchi_key,
            )

            insert_properties(
                conn,
                molecule_id=db_id,
                run_id=req.run_id or "api",
                props=props,
            )

            insert_fingerprint(
                conn,
                molecule_id=db_id,
                fingerprint=fp_str,
            )

            conn.commit()

        finally:
            conn.close()

    return NormalizeResponse(

      ok=True,

      smiles_canonico=v.smiles,

      inchi=v.inchi,

      inchi_key=v.inchi_key,

      iupac_name=iupac_name,

      properties=props,

      db_molecule_id=db_id,
    )


# -----------------------------
# SIMILARIDADE DIRETA
# -----------------------------
@app.post("/molecules/similarity")
def similarity(req: SimilarityRequest):

    return compute_similarity(
        req.smiles_a,
        req.smiles_b
    )


# -----------------------------
# BUSCA NO BANCO
# -----------------------------
@app.post("/molecules/search_similar")
def search(req: SearchRequest):

    results = search_similar(
        smiles=req.smiles,
        top_k=req.top_k
    )

    return {
        "query": req.smiles,
        "results": results
    }


# -----------------------------
# BUSCA POR INCHIKEY (GENÉRICA - POR ÚLTIMO)
# -----------------------------
@app.get("/molecules/{inchi_key}")
def get_molecule(inchi_key: str):

    conn = get_connection()

    try:
        mol = get_molecule_by_inchikey(conn, inchi_key)

        if not mol:
            raise HTTPException(
                status_code=404,
                detail="Molécula não encontrada"
            )

        props = get_properties_for_molecule(conn, mol["id"])

        return {
            "molecule": mol,
            "properties": props,
        }

    finally:
        conn.close()