from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import os

def gerar_relatorio(caminho_pdf="outputs/relatorio_visualizacoes.pdf"):
    os.makedirs("outputs", exist_ok=True)

    doc = SimpleDocTemplate(caminho_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    conteudo = []

    conteudo.append(Paragraph("Relatório de Visualização Molecular", styles["Title"]))
    conteudo.append(Spacer(1, 12))

    conteudo.append(Paragraph(
        "Este relatório apresenta o painel de moléculas, gráficos de propriedades "
        "e resumo das etapas realizadas até o momento.", styles["BodyText"]
    ))
    conteudo.append(Spacer(1, 12))

    if os.path.exists("outputs/painel_moleculas.png"):
        conteudo.append(Image("outputs/painel_moleculas.png", width=14*cm, height=14*cm))
        conteudo.append(Spacer(1, 12))

    if os.path.exists("outputs/graficos/logp_vs_tpsa.png"):
        conteudo.append(Paragraph("Gráfico: LogP x TPSA", styles["Heading2"]))
        conteudo.append(Image("outputs/graficos/logp_vs_tpsa.png", width=14*cm, height=10*cm))
        conteudo.append(Spacer(1, 12))

    if os.path.exists("outputs/graficos/molwt_vs_logp.png"):
        conteudo.append(Paragraph("Gráfico: MolWt x LogP", styles["Heading2"]))
        conteudo.append(Image("outputs/graficos/molwt_vs_logp.png", width=14*cm, height=10*cm))
        conteudo.append(Spacer(1, 12))

    doc.build(conteudo)
    print("✓ PDF gerado em:", caminho_pdf)

if __name__ == "__main__":
    gerar_relatorio()
