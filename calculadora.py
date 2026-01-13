"""
Logica de calculo das retencoes conforme IN RFB 1.234/2012
"""

from datetime import date, timedelta
from typing import Optional
from dataclasses import dataclass
from dados_in1234 import (
    CODIGOS_DARF,
    NATUREZAS_SERVICO,
    TIPOS_DISPENSA_RETENCAO,
    VALOR_MINIMO_RETENCAO,
    DIA_RECOLHIMENTO
)


@dataclass
class ResultadoRetencao:
    """Resultado do calculo de retencao"""
    valor_bruto: float
    valor_ir: float
    valor_csll: float
    valor_cofins: float
    valor_pis_pasep: float
    valor_total_retido: float
    valor_liquido: float
    codigo_darf: str
    descricao_darf: str
    aliquota_total: float
    data_recolhimento: date
    dispensa_retencao: bool
    motivo_dispensa: Optional[str] = None


def calcular_data_recolhimento(data_pagamento: date) -> date:
    """
    Calcula a data limite para recolhimento.
    Ate o dia 20 do mes subsequente ao pagamento.
    """
    # Proximo mes
    if data_pagamento.month == 12:
        proximo_mes = 1
        ano = data_pagamento.year + 1
    else:
        proximo_mes = data_pagamento.month + 1
        ano = data_pagamento.year

    # Dia 20 do proximo mes
    return date(ano, proximo_mes, DIA_RECOLHIMENTO)


def verificar_dispensa_retencao(
    valor: float,
    regime_tributario: str,
    tipo_fornecedor: str
) -> tuple[bool, Optional[str]]:
    """
    Verifica se ha dispensa de retencao.

    Retorna:
        tuple: (dispensa, motivo)
    """
    # Valor igual ou inferior a R$ 10,00
    if valor <= VALOR_MINIMO_RETENCAO:
        return True, f"Valor igual ou inferior a R$ {VALOR_MINIMO_RETENCAO:.2f}"

    # Simples Nacional
    if regime_tributario == "Simples Nacional":
        return True, "Empresa optante pelo Simples Nacional"

    # Tipos especiais de fornecedor
    if tipo_fornecedor in TIPOS_DISPENSA_RETENCAO:
        return True, f"Fornecedor: {tipo_fornecedor}"

    return False, None


def calcular_retencao(
    valor_bruto: float,
    natureza_servico: str,
    data_pagamento: date,
    regime_tributario: str = "Lucro Real",
    tipo_fornecedor: str = "Normal"
) -> ResultadoRetencao:
    """
    Calcula as retencoes de tributos federais conforme IN RFB 1.234/2012.

    Args:
        valor_bruto: Valor total da fatura/nota fiscal
        natureza_servico: Natureza do servico prestado
        data_pagamento: Data do pagamento
        regime_tributario: Regime tributario do fornecedor
        tipo_fornecedor: Tipo especial do fornecedor (se aplicavel)

    Returns:
        ResultadoRetencao: Objeto com todos os valores calculados
    """
    # Verificar dispensa
    dispensa, motivo = verificar_dispensa_retencao(
        valor_bruto, regime_tributario, tipo_fornecedor
    )

    # Obter codigo DARF
    codigo_darf = NATUREZAS_SERVICO.get(natureza_servico, "6190")
    dados_darf = CODIGOS_DARF[codigo_darf]

    # Calcular data de recolhimento
    data_recolhimento = calcular_data_recolhimento(data_pagamento)

    if dispensa:
        # Sem retencao
        return ResultadoRetencao(
            valor_bruto=valor_bruto,
            valor_ir=0.0,
            valor_csll=0.0,
            valor_cofins=0.0,
            valor_pis_pasep=0.0,
            valor_total_retido=0.0,
            valor_liquido=valor_bruto,
            codigo_darf=codigo_darf,
            descricao_darf=dados_darf["descricao"],
            aliquota_total=dados_darf["aliquota_total"],
            data_recolhimento=data_recolhimento,
            dispensa_retencao=True,
            motivo_dispensa=motivo
        )

    # Calcular retencoes
    aliquotas = dados_darf["aliquotas"]

    valor_ir = round(valor_bruto * aliquotas["IR"], 2)
    valor_csll = round(valor_bruto * aliquotas["CSLL"], 2)
    valor_cofins = round(valor_bruto * aliquotas["COFINS"], 2)
    valor_pis_pasep = round(valor_bruto * aliquotas["PIS_PASEP"], 2)

    valor_total_retido = round(valor_ir + valor_csll + valor_cofins + valor_pis_pasep, 2)
    valor_liquido = round(valor_bruto - valor_total_retido, 2)

    return ResultadoRetencao(
        valor_bruto=valor_bruto,
        valor_ir=valor_ir,
        valor_csll=valor_csll,
        valor_cofins=valor_cofins,
        valor_pis_pasep=valor_pis_pasep,
        valor_total_retido=valor_total_retido,
        valor_liquido=valor_liquido,
        codigo_darf=codigo_darf,
        descricao_darf=dados_darf["descricao"],
        aliquota_total=dados_darf["aliquota_total"],
        data_recolhimento=data_recolhimento,
        dispensa_retencao=False
    )
