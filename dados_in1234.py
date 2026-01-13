"""
Dados e constantes da IN RFB 1.234/2012
Retencao de tributos federais por orgaos publicos
"""

# Aliquotas por tributo (em decimal)
ALIQUOTAS = {
    "IR": 0.048,      # 4,80%
    "CSLL": 0.01,     # 1,00%
    "COFINS": 0.03,   # 3,00%
    "PIS_PASEP": 0.0065  # 0,65%
}

# Codigos DARF e suas configuracoes
CODIGOS_DARF = {
    "6147": {
        "descricao": "Servicos com emprego de materiais",
        "aliquota_total": 0.0585,
        "aliquotas": {
            "IR": 0.012,      # 1,20%
            "CSLL": 0.01,     # 1,00%
            "COFINS": 0.03,   # 3,00%
            "PIS_PASEP": 0.0065  # 0,65%
        }
    },
    "6190": {
        "descricao": "Demais servicos (telefonia, etc.)",
        "aliquota_total": 0.0945,
        "aliquotas": {
            "IR": 0.048,      # 4,80%
            "CSLL": 0.01,     # 1,00%
            "COFINS": 0.03,   # 3,00%
            "PIS_PASEP": 0.0065  # 0,65%
        }
    },
    "8739": {
        "descricao": "Servicos de limpeza e conservacao",
        "aliquota_total": 0.0585,
        "aliquotas": {
            "IR": 0.012,      # 1,20%
            "CSLL": 0.01,     # 1,00%
            "COFINS": 0.03,   # 3,00%
            "PIS_PASEP": 0.0065  # 0,65%
        }
    },
    "8767": {
        "descricao": "Servicos de vigilancia",
        "aliquota_total": 0.0585,
        "aliquotas": {
            "IR": 0.012,      # 1,20%
            "CSLL": 0.01,     # 1,00%
            "COFINS": 0.03,   # 3,00%
            "PIS_PASEP": 0.0065  # 0,65%
        }
    }
}

# Naturezas de servico mapeadas para codigos DARF
NATUREZAS_SERVICO = {
    "Servicos com emprego de materiais": "6147",
    "Telefonia": "6190",
    "Demais servicos": "6190",
    "Limpeza e conservacao": "8739",
    "Vigilancia": "8767"
}

# Tipos de fornecedor com dispensa de retencao
TIPOS_DISPENSA_RETENCAO = [
    "Simples Nacional",
    "Instituicao de educacao sem fins lucrativos",
    "Instituicao de assistencia social sem fins lucrativos",
    "Instituicao filantropica",
    "Instituicao recreativa sem fins lucrativos",
    "Instituicao cultural sem fins lucrativos",
    "Instituicao cientifica sem fins lucrativos",
    "Fundacao publica mantida pelo Poder Publico",
    "Cooperativa (OCB)"
]

# Regimes tributarios
REGIMES_TRIBUTARIOS = [
    "Simples Nacional",
    "Lucro Real",
    "Lucro Presumido",
    "Lucro Arbitrado"
]

# Valor minimo para retencao (em reais)
VALOR_MINIMO_RETENCAO = 10.00

# Dia do mes para recolhimento
DIA_RECOLHIMENTO = 20
