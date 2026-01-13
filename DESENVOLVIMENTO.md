# Passo-a-Passo do Desenvolvimento

Documentacao completa do desenvolvimento do sistema **Calculadora de Retencao de Tributos - IN RFB 1.234/2012**.

---

## 1. Analise do Requisito

### 1.1 Documento Base
Foi fornecido o PDF da **Instrucao Normativa RFB 1.234/2012** contendo:
- Quem deve reter tributos (orgaos publicos)
- Tributos retidos: IR, CSLL, COFINS, PIS/PASEP
- Hipoteses de nao retencao (Simples Nacional, cooperativas, etc.)
- Dispensa de retencao (valores <= R$ 10,00)
- Codigos DARF e aliquotas
- Prazo de recolhimento (dia 20 do mes subsequente)

### 1.2 Requisitos Definidos
- Sistema web usando Streamlit
- Entrada de dados do fornecedor e pagamento
- Calculo automatico das retencoes
- Exibicao de valores, codigo DARF e prazo de recolhimento
- Deploy na nuvem

---

## 2. Estrutura do Projeto

### 2.1 Local de Armazenamento
```
c:\Projetos\estudos\projeto-1\calculadora_retencao\
```

### 2.2 Arquivos Criados
```
calculadora_retencao/
├── app.py              # Interface Streamlit
├── calculadora.py      # Logica de calculo
├── dados_in1234.py     # Constantes e dados da IN 1.234/2012
├── requirements.txt    # Dependencias Python
├── README.md           # Documentacao do projeto
├── DESENVOLVIMENTO.md  # Este arquivo
└── .gitignore          # Arquivos ignorados pelo Git
```

---

## 3. Implementacao

### 3.1 Modulo de Dados (`dados_in1234.py`)

Contem todas as constantes baseadas na IN 1.234/2012:

```python
# Aliquotas por tributo
ALIQUOTAS = {
    "IR": 0.048,        # 4,80%
    "CSLL": 0.01,       # 1,00%
    "COFINS": 0.03,     # 3,00%
    "PIS_PASEP": 0.0065 # 0,65%
}

# Codigos DARF suportados
CODIGOS_DARF = {
    "6147": {...},  # Servicos com emprego de materiais (5,85%)
    "6190": {...},  # Demais servicos/telefonia (9,45%)
    "8739": {...},  # Limpeza e conservacao (5,85%)
    "8767": {...}   # Vigilancia (5,85%)
}

# Tipos com dispensa de retencao
TIPOS_DISPENSA_RETENCAO = [
    "Simples Nacional",
    "Instituicao de educacao sem fins lucrativos",
    # ... outros tipos
]

# Valor minimo para retencao
VALOR_MINIMO_RETENCAO = 10.00

# Dia do recolhimento
DIA_RECOLHIMENTO = 20
```

### 3.2 Modulo de Calculo (`calculadora.py`)

Implementa a logica de negocio:

```python
@dataclass
class ResultadoRetencao:
    valor_bruto: float
    valor_ir: float
    valor_csll: float
    valor_cofins: float
    valor_pis_pasep: float
    valor_total_retido: float
    valor_liquido: float
    codigo_darf: str
    # ... outros campos

def calcular_retencao(valor_bruto, natureza_servico, data_pagamento, ...):
    # 1. Verifica dispensa de retencao
    # 2. Obtem codigo DARF pela natureza do servico
    # 3. Calcula cada tributo
    # 4. Calcula data de recolhimento
    # 5. Retorna ResultadoRetencao
```

### 3.3 Interface Streamlit (`app.py`)

Estrutura da interface:

1. **Cabecalho**: Titulo e descricao
2. **Coluna 1 - Dados do Fornecedor**:
   - CNPJ (opcional)
   - Razao Social (opcional)
   - Regime Tributario
   - Tipo de Fornecedor
3. **Coluna 2 - Dados do Pagamento**:
   - Valor Bruto
   - Natureza do Servico
   - Data do Pagamento
4. **Botao Calcular**
5. **Resultado**:
   - Metricas principais (bruto, retido, liquido)
   - Tabela de tributos
   - Informacoes para recolhimento
   - Resumo para impressao

---

## 4. Ambiente de Desenvolvimento

### 4.1 Criar Ambiente Virtual
```bash
cd c:\Projetos\estudos\projeto-1\calculadora_retencao
python -m venv venv
```

### 4.2 Ativar Ambiente Virtual
```bash
# Windows
venv\Scripts\activate
```

### 4.3 Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4.4 Executar Localmente
```bash
streamlit run app.py
```

Acesso local: **http://localhost:8501**

---

## 5. Versionamento com Git

### 5.1 Criar .gitignore
```
venv/
__pycache__/
*.py[cod]
.vscode/
.streamlit/secrets.toml
```

### 5.2 Inicializar Repositorio
```bash
git init
git add .
git commit -m "Calculadora de Retencao IN RFB 1.234/2012"
```

---

## 6. Deploy na Nuvem (Streamlit Cloud)

### 6.1 Pre-requisitos
- Conta no GitHub
- GitHub CLI instalado (opcional, facilita o processo)

### 6.2 Instalar GitHub CLI (Windows)
```bash
winget install --id GitHub.cli
```

### 6.3 Autenticar no GitHub
```bash
gh auth login --web -h github.com
```
- Acessar https://github.com/login/device
- Inserir o codigo exibido no terminal
- Autorizar acesso

### 6.4 Criar Repositorio e Fazer Push
```bash
gh repo create calculadora-retencao-in1234 \
  --public \
  --description "Calculadora de Retencao de Tributos - IN RFB 1.234/2012" \
  --source . \
  --push
```

Repositorio criado: `https://github.com/SEU_USUARIO/calculadora-retencao-in1234`

### 6.5 Deploy no Streamlit Cloud

1. Acessar **https://share.streamlit.io**
2. Fazer login com GitHub
3. Clicar em **New app**
4. Configurar:
   - **Repository:** `SEU_USUARIO/calculadora-retencao-in1234`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Clicar em **Deploy!**

Aguardar 2-3 minutos para o deploy completar.

**URL final:** `https://calculadora-retencao-in1234.streamlit.app`

---

## 7. Resultado Final

### 7.1 Funcionalidades Implementadas
- [x] Entrada de dados do fornecedor (CNPJ, razao social, regime tributario)
- [x] Entrada de dados do pagamento (valor, natureza, data)
- [x] Verificacao automatica de dispensa de retencao
- [x] Calculo de IR, CSLL, COFINS e PIS/PASEP
- [x] Exibicao do codigo DARF correto
- [x] Calculo da data limite de recolhimento
- [x] Resumo para impressao
- [x] Deploy na nuvem

### 7.2 Codigos DARF Suportados

| Codigo | Natureza | Aliquota Total |
|--------|----------|----------------|
| 6147 | Servicos com emprego de materiais | 5,85% |
| 6190 | Demais servicos (telefonia, etc.) | 9,45% |
| 8739 | Servicos de limpeza e conservacao | 5,85% |
| 8767 | Servicos de vigilancia | 5,85% |

### 7.3 Links

- **Aplicacao:** https://calculadora-retencao-in1234.streamlit.app
- **Repositorio:** https://github.com/gabrielgscm1/calculadora-retencao-in1234

---

## 8. Proximos Passos (Sugestoes)

- [ ] Adicionar mais codigos DARF do Anexo I
- [ ] Exportar resultado em PDF
- [ ] Historico de calculos
- [ ] Validacao de CNPJ
- [ ] Integracao com banco de dados

---

*Documento criado em: 13/01/2026*
