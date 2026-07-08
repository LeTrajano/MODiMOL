from rdkit.Chem import Draw
import pandas as pd
import os

from src.chemistry.validation import validate_smiles
from src.models import ValidationError


def gerar_visualizacoes(
    csv_entrada="data/propriedades_avancadas.csv",
    pasta_imagens="outputs",
    csv_saida="outputs/propriedades_com_imagens.csv",
    painel_saida="outputs/painel_moleculas.png",
    mols_por_linha=4
):
    os.makedirs(pasta_imagens, exist_ok=True)
    os.makedirs(os.path.dirname(csv_saida), exist_ok=True)

    df = pd.read_csv(csv_entrada)

    caminhos_imagens = []
    moleculas = []
    legends = []
    erros = []

    print("▶ Gerando imagens individuais...")

    for idx, row in df.iterrows():
        smi = row["SMILES"]          # agora é canônico
        mol_id = row["mol_id"]

        v = validate_smiles(smi)
        if isinstance(v, ValidationError):
            caminhos_imagens.append("ERRO")
            erros.append({
                "mol_id": mol_id,
                "SMILES": smi,
                "reason": v.reason,
                "details": v.details or {}
            })
            continue

        nome_arquivo = f"{mol_id}.png"
        caminho_completo = os.path.join(pasta_imagens, nome_arquivo)

        img = Draw.MolToImage(v.mol, size=(300, 300))
        img.save(caminho_completo)

        caminhos_imagens.append(caminho_completo)
        moleculas.append(v.mol)
        legends.append(str(mol_id))

    df["caminho_imagem"] = caminhos_imagens
    df.to_csv(csv_saida, index=False)

    print("▶ Criando painel (grid) de moléculas...")

    if moleculas:
        img_grid = Draw.MolsToGridImage(
            moleculas,
            molsPerRow=mols_por_linha,
            subImgSize=(250, 250),
            legends=legends
        )
        img_grid.save(painel_saida)
        print("✓ Painel salvo em:", painel_saida)
    else:
        print("⚠ Nenhuma molécula válida para painel.")

    if erros:
        df_err = pd.DataFrame(erros)
        df_err.to_csv("outputs/erros_visualizacao.csv", index=False)
        print("⚠ Erros de visualização salvos em: outputs/erros_visualizacao.csv")

    print("\n✓ Visualização molecular concluída!")
    print("• CSV gerado em:", csv_saida)
    print("• Imagens salvas em:", pasta_imagens)


if __name__ == "__main__":
    gerar_visualizacoes()