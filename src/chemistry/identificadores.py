# src/chemistry/identificadores.py

def gerar_id_local(indice: int, prefixo: str = "MOL") -> str:
    """
    Gera um identificador local estável para moléculas.

    Exemplo:
        indice=0  -> MOL_0000
        indice=12 -> MOL_0012
    """
    return f"{prefixo}_{indice:04d}"