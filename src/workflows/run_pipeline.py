import argparse
import os

from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Workflow canônico do projeto molecular (pipeline + artefatos opcionais)."
    )

    parser.add_argument("--input", default="data/propriedades_pipeline.csv",
                        help="CSV de entrada (default: data/propriedades_pipeline.csv)")
    parser.add_argument("--out", default="data/propriedades_avancadas.csv",
                        help="CSV de saída principal (default: data/propriedades_avancadas.csv)")

    parser.add_argument("--images", action="store_true", help="Gerar imagens moleculares e painel")
    parser.add_argument("--plots", action="store_true", help="Gerar gráficos de propriedades")
    parser.add_argument("--pdf", action="store_true", help="Gerar relatório PDF (depende de imagens/plots)")
    parser.add_argument("--similarity", action="store_true", help="Rodar similaridade e salvar CSV")
    parser.add_argument("--clustering", action="store_true", help="Rodar clustering e salvar CSV")

    parser.add_argument("--clusters", type=int, default=3, help="Número de clusters (default: 3)")
    parser.add_argument("--ref_smiles", default=None,
                        help="SMILES de referência para similaridade (se omitido, usa a primeira molécula do CSV).")

    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print("▶ Executando pipeline básico...")
    from src.scripts.pipeline_basico import pipeline as run_basic
    df_out = run_basic(csv_entrada=args.input, csv_saida=args.out)

    # Imagens
    if args.images:
        print("\n▶ Gerando visualizações...")
        from src.scripts.visualizacoes import gerar_visualizacoes
        gerar_visualizacoes(csv_entrada=args.out)

    # Gráficos
    if args.plots:
        print("\n▶ Gerando gráficos...")
        from src.scripts.plots_propriedades import gerar_graficos # type: ignore
        gerar_graficos(csv=args.out, pasta="outputs/graficos")

    # PDF (opcional)
    if args.pdf:
        print("\n▶ Gerando relatório PDF...")
        # Se seu relatorio_visualizacoes.py já espera caminhos específicos, mantenha
        from src.scripts.relatorio_visualizacoes import gerar_relatorio_pdf
        gerar_relatorio_pdf()

    # Similaridade
    if args.similarity:
        print("\n▶ Rodando similaridade...")
        import pandas as pd
        from src.scripts.similaridade import calcular_similaridade

        df = pd.read_csv(args.out)
        if df.empty:
            print("⚠ CSV vazio. Pulando similaridade.")
        else:
            ref = args.ref_smiles or df["SMILES"].iloc[0]
            sim = calcular_similaridade(df["SMILES"].tolist(), ref)
            sim.to_csv("outputs/similaridade_resultado.csv", index=False)
            print("✓ Similaridade salva em outputs/similaridade_resultado.csv")

    # Clustering
    if args.clustering:
        print("\n▶ Rodando clustering...")
        import pandas as pd
        from src.scripts.clustering import gerar_clustering
        df = pd.read_csv(args.out)
        out = gerar_clustering(df, n_clusters=args.clusters)
        print(f"✓ Clustering salvo em outputs/clustering_resultado.csv ({len(out)} linhas)")
       
        # --- Export automático do dataset do run ---
    try:
        from src.persistence.database import get_connection
        from src.persistence.query_runs import dataset_for_run, latest_dataset

        conn = get_connection()
        try:
            # se você guardou run_id no pipeline_basico, recomendo retornar run_id também
            # mas, como já imprimimos, vamos pegar o latest como fallback
            df_latest = latest_dataset(conn)
            Path("outputs").mkdir(exist_ok=True)

            df_latest.to_csv("outputs/dataset_latest.csv", index=False)

            # tentar inferir run_id mais recente
            run = conn.execute("""
                SELECT run_id
                FROM properties
                GROUP BY run_id
                ORDER BY MAX(created_at) DESC
                LIMIT 1
            """).fetchone()

            if run:
                df_run = dataset_for_run(conn, run["run_id"])
                df_run.to_csv(f"outputs/dataset_{run['run_id']}.csv", index=False)
                Path("outputs/last_run_id.txt").write_text(run["run_id"], encoding="utf-8")

                print(f"✓ Dataset do run salvo em: outputs/dataset_{run['run_id']}.csv")
                print("✓ Dataset latest salvo em: outputs/dataset_latest.csv")
                print("✓ last_run_id.txt atualizado.")
        finally:
            conn.close()
    except Exception as e:
        print("⚠ Não foi possível exportar dataset automaticamente:", e)
    
    print("\n✅ Workflow finalizado com sucesso.")


if __name__ == "__main__":
    main()