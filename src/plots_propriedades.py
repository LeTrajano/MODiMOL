import pandas as pd
import matplotlib.pyplot as plt
import os

def gerar_graficos(csv="data/propriedades_avancadas.csv", pasta="outputs/graficos"):
    os.makedirs(pasta, exist_ok=True)
    df = pd.read_csv(csv)

    print("▶ Gerando gráficos...")

    # 1 — LogP x TPSA
    plt.scatter(df["LogP"], df["TPSA"])
    plt.xlabel("LogP")
    plt.ylabel("TPSA")
    plt.title("LogP x TPSA")
    plt.savefig(f"{pasta}/logp_vs_tpsa.png")
    plt.close()

    # 2 — MolWt x LogP
    plt.scatter(df["MolWt"], df["LogP"])
    plt.xlabel("Peso Molecular (MolWt)")
    plt.ylabel("LogP")
    plt.title("MolWt x LogP")
    plt.savefig(f"{pasta}/molwt_vs_logp.png")
    plt.close()

    # 3 — Histograma de Peso Molecular
    plt.hist(df["MolWt"])
    plt.xlabel("Peso Molecular")
    plt.ylabel("Frequência")
    plt.title("Distribuição do Peso Molecular")
    plt.savefig(f"{pasta}/hist_molwt.png")
    plt.close()

    print("✓ Gráficos salvos em:", pasta)

if __name__ == "__main__":
    gerar_graficos()
