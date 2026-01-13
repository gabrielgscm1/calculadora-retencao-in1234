"""
Geracao de PDF com o resultado do calculo de retencao
"""

from fpdf import FPDF
from datetime import date
from calculadora import ResultadoRetencao
from dados_in1234 import CODIGOS_DARF


class PDFRetencao(FPDF):
    """Classe customizada para gerar PDF de retencao"""

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Calculadora de Retencao de Tributos", align="C", ln=True)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, "Instrucao Normativa RFB 1.234/2012", align="C", ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Gerado em: {date.today().strftime('%d/%m/%Y')}", align="C")


def gerar_pdf(
    resultado: ResultadoRetencao,
    cnpj: str = "",
    razao_social: str = "",
    regime_tributario: str = "",
    natureza_servico: str = "",
    data_pagamento: date = None
) -> bytes:
    """
    Gera PDF com o resultado do calculo de retencao.

    Args:
        resultado: Objeto ResultadoRetencao com os valores calculados
        cnpj: CNPJ do fornecedor
        razao_social: Razao social do fornecedor
        regime_tributario: Regime tributario
        natureza_servico: Natureza do servico
        data_pagamento: Data do pagamento

    Returns:
        bytes: Conteudo do PDF em bytes
    """
    pdf = PDFRetencao()
    pdf.add_page()

    # Dados do Fornecedor
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Dados do Fornecedor", ln=True)
    pdf.set_font("Helvetica", "", 10)

    pdf.cell(40, 6, "CNPJ:", border=0)
    pdf.cell(0, 6, cnpj or "Nao informado", ln=True)

    pdf.cell(40, 6, "Razao Social:", border=0)
    pdf.cell(0, 6, razao_social or "Nao informado", ln=True)

    pdf.cell(40, 6, "Regime Tributario:", border=0)
    pdf.cell(0, 6, regime_tributario, ln=True)

    pdf.ln(5)

    # Dados do Pagamento
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Dados do Pagamento", ln=True)
    pdf.set_font("Helvetica", "", 10)

    pdf.cell(40, 6, "Natureza:", border=0)
    pdf.cell(0, 6, natureza_servico, ln=True)

    pdf.cell(40, 6, "Data Pagamento:", border=0)
    pdf.cell(0, 6, data_pagamento.strftime("%d/%m/%Y") if data_pagamento else "", ln=True)

    pdf.cell(40, 6, "Valor Bruto:", border=0)
    pdf.cell(0, 6, f"R$ {resultado.valor_bruto:,.2f}", ln=True)

    pdf.ln(5)

    # Alerta de dispensa
    if resultado.dispensa_retencao:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(255, 255, 200)
        pdf.cell(0, 8, f"DISPENSA DE RETENCAO: {resultado.motivo_dispensa}", fill=True, ln=True)
        pdf.ln(5)

    # Tabela de Tributos
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Tributos Retidos", ln=True)

    # Cabecalho da tabela
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(80, 7, "Tributo", border=1, fill=True)
    pdf.cell(40, 7, "Aliquota", border=1, fill=True, align="C")
    pdf.cell(50, 7, "Valor (R$)", border=1, fill=True, align="R")
    pdf.ln()

    # Dados da tabela
    pdf.set_font("Helvetica", "", 10)
    aliquotas = CODIGOS_DARF[resultado.codigo_darf]["aliquotas"]

    tributos = [
        ("IR (Imposto de Renda)", aliquotas["IR"], resultado.valor_ir),
        ("CSLL", aliquotas["CSLL"], resultado.valor_csll),
        ("COFINS", aliquotas["COFINS"], resultado.valor_cofins),
        ("PIS/PASEP", aliquotas["PIS_PASEP"], resultado.valor_pis_pasep),
    ]

    for nome, aliquota, valor in tributos:
        pdf.cell(80, 7, nome, border=1)
        pdf.cell(40, 7, f"{aliquota * 100:.2f}%", border=1, align="C")
        pdf.cell(50, 7, f"{valor:,.2f}", border=1, align="R")
        pdf.ln()

    # Total
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(80, 7, "TOTAL RETIDO", border=1, fill=True)
    pdf.cell(40, 7, f"{resultado.aliquota_total * 100:.2f}%", border=1, fill=True, align="C")
    pdf.cell(50, 7, f"{resultado.valor_total_retido:,.2f}", border=1, fill=True, align="R")
    pdf.ln()

    pdf.ln(5)

    # Resumo
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Resumo", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(60, 7, "Valor Bruto:", border=0)
    pdf.cell(0, 7, f"R$ {resultado.valor_bruto:,.2f}", ln=True)

    pdf.cell(60, 7, "Total Retido:", border=0)
    pdf.cell(0, 7, f"R$ {resultado.valor_total_retido:,.2f}", ln=True)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(60, 7, "Valor Liquido a Pagar:", border=0)
    pdf.cell(0, 7, f"R$ {resultado.valor_liquido:,.2f}", ln=True)

    pdf.ln(5)

    # Informacoes para Recolhimento
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Informacoes para Recolhimento", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(60, 7, "Codigo DARF:", border=0)
    pdf.cell(0, 7, resultado.codigo_darf, ln=True)

    pdf.cell(60, 7, "Natureza:", border=0)
    pdf.cell(0, 7, resultado.descricao_darf, ln=True)

    pdf.cell(60, 7, "Data Limite Recolhimento:", border=0)
    pdf.cell(0, 7, resultado.data_recolhimento.strftime("%d/%m/%Y"), ln=True)

    # Retorna o PDF como bytes
    return pdf.output()
