# Calculadora de Retencao de Tributos - IN RFB 1.234/2012

Sistema para calculo de retencao de tributos federais conforme Instrucao Normativa RFB 1.234/2012.

## Funcionalidades

- Calculo automatico de IR, CSLL, COFINS e PIS/PASEP
- Verificacao de dispensa de retencao (Simples Nacional, valores <= R$ 10,00, etc.)
- Selecao de natureza do servico com codigo DARF correspondente
- Calculo automatico da data limite para recolhimento
- Resumo para impressao

## Instalacao

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Execucao

```bash
streamlit run app.py
```

## Estrutura

```
calculadora_retencao/
├── app.py              # Interface Streamlit
├── calculadora.py      # Logica de calculo
├── dados_in1234.py     # Constantes e dados da IN 1.234/2012
├── requirements.txt    # Dependencias
└── README.md           # Este arquivo
```

## Codigos DARF Suportados

| Codigo | Natureza | Aliquota |
|--------|----------|----------|
| 6147 | Servicos com emprego de materiais | 5,85% |
| 6190 | Demais servicos (telefonia, etc.) | 9,45% |
| 8739 | Servicos de limpeza e conservacao | 5,85% |
| 8767 | Servicos de vigilancia | 5,85% |

## Referencias

- IN RFB 1.234/2012
- IN RFB 2.145/2023
- IN RFB 2.239/2024
