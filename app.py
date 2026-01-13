"""
Calculadora de Retencao de Tributos - IN RFB 1.234/2012
Interface Streamlit
"""

import streamlit as st
from datetime import date
from calculadora import calcular_retencao
from dados_in1234 import (
    NATUREZAS_SERVICO,
    REGIMES_TRIBUTARIOS,
    TIPOS_DISPENSA_RETENCAO,
    CODIGOS_DARF
)

# Configuracao da pagina
st.set_page_config(
    page_title="Calculadora IN RFB 1.234/2012",
    page_icon="🧮",
    layout="wide"
)

# Titulo
st.title("🧮 Calculadora de Retencao de Tributos")
st.markdown("**Instrucao Normativa RFB 1.234/2012**")
st.markdown("---")

# Layout em colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Dados do Fornecedor")

    cnpj = st.text_input(
        "CNPJ",
        placeholder="00.000.000/0000-00",
        help="CNPJ do fornecedor (opcional)"
    )

    razao_social = st.text_input(
        "Razao Social",
        placeholder="Nome da empresa",
        help="Razao social do fornecedor (opcional)"
    )

    regime_tributario = st.selectbox(
        "Regime Tributario",
        options=REGIMES_TRIBUTARIOS,
        index=1,  # Lucro Real como padrao
        help="Regime tributario do fornecedor"
    )

    tipo_fornecedor = st.selectbox(
        "Tipo de Fornecedor",
        options=["Normal"] + TIPOS_DISPENSA_RETENCAO,
        help="Selecione se o fornecedor possui algum tipo especial com dispensa"
    )

with col2:
    st.subheader("💰 Dados do Pagamento")

    valor_bruto = st.number_input(
        "Valor Bruto (R$)",
        min_value=0.0,
        value=1000.0,
        step=0.01,
        format="%.2f",
        help="Valor total da fatura/nota fiscal"
    )

    natureza_servico = st.selectbox(
        "Natureza do Servico",
        options=list(NATUREZAS_SERVICO.keys()),
        help="Tipo de servico prestado"
    )

    data_pagamento = st.date_input(
        "Data do Pagamento",
        value=date.today(),
        help="Data em que o pagamento sera efetuado"
    )

st.markdown("---")

# Botao de calculo
if st.button("🔢 Calcular Retencao", type="primary", use_container_width=True):

    if valor_bruto <= 0:
        st.error("O valor bruto deve ser maior que zero.")
    else:
        # Realizar calculo
        resultado = calcular_retencao(
            valor_bruto=valor_bruto,
            natureza_servico=natureza_servico,
            data_pagamento=data_pagamento,
            regime_tributario=regime_tributario,
            tipo_fornecedor=tipo_fornecedor
        )

        st.markdown("---")
        st.subheader("📊 Resultado do Calculo")

        # Alerta de dispensa
        if resultado.dispensa_retencao:
            st.warning(f"⚠️ **DISPENSA DE RETENCAO**: {resultado.motivo_dispensa}")

        # Metricas principais
        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric("Valor Bruto", f"R$ {resultado.valor_bruto:,.2f}")
        with col_r2:
            st.metric("Total Retido", f"R$ {resultado.valor_total_retido:,.2f}")
        with col_r3:
            st.metric("Valor Liquido", f"R$ {resultado.valor_liquido:,.2f}")

        st.markdown("---")

        # Detalhamento dos tributos
        col_t1, col_t2 = st.columns(2)

        with col_t1:
            st.subheader("📑 Tributos Retidos")

            # Tabela de tributos
            dados_tributos = {
                "Tributo": ["IR (Imposto de Renda)", "CSLL", "COFINS", "PIS/PASEP", "**TOTAL**"],
                "Aliquota": [
                    f"{CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['IR'] * 100:.2f}%",
                    f"{CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['CSLL'] * 100:.2f}%",
                    f"{CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['COFINS'] * 100:.2f}%",
                    f"{CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['PIS_PASEP'] * 100:.2f}%",
                    f"**{resultado.aliquota_total * 100:.2f}%**"
                ],
                "Valor (R$)": [
                    f"{resultado.valor_ir:,.2f}",
                    f"{resultado.valor_csll:,.2f}",
                    f"{resultado.valor_cofins:,.2f}",
                    f"{resultado.valor_pis_pasep:,.2f}",
                    f"**{resultado.valor_total_retido:,.2f}**"
                ]
            }

            st.table(dados_tributos)

        with col_t2:
            st.subheader("🏦 Informacoes para Recolhimento")

            st.info(f"""
            **Codigo DARF:** {resultado.codigo_darf}

            **Natureza:** {resultado.descricao_darf}

            **Data Limite:** {resultado.data_recolhimento.strftime('%d/%m/%Y')}

            **Aliquota Total:** {resultado.aliquota_total * 100:.2f}%
            """)

        # Resumo para impressao
        st.markdown("---")
        with st.expander("📄 Resumo para Impressao"):
            st.markdown(f"""
            ### Calculadora de Retencao - IN RFB 1.234/2012

            **Fornecedor:** {razao_social or 'Nao informado'} ({cnpj or 'CNPJ nao informado'})

            **Regime Tributario:** {regime_tributario}

            **Natureza do Servico:** {natureza_servico}

            **Data do Pagamento:** {data_pagamento.strftime('%d/%m/%Y')}

            ---

            | Item | Valor |
            |------|-------|
            | Valor Bruto | R$ {resultado.valor_bruto:,.2f} |
            | IR ({CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['IR'] * 100:.2f}%) | R$ {resultado.valor_ir:,.2f} |
            | CSLL ({CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['CSLL'] * 100:.2f}%) | R$ {resultado.valor_csll:,.2f} |
            | COFINS ({CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['COFINS'] * 100:.2f}%) | R$ {resultado.valor_cofins:,.2f} |
            | PIS/PASEP ({CODIGOS_DARF[resultado.codigo_darf]['aliquotas']['PIS_PASEP'] * 100:.2f}%) | R$ {resultado.valor_pis_pasep:,.2f} |
            | **Total Retido** | **R$ {resultado.valor_total_retido:,.2f}** |
            | **Valor Liquido** | **R$ {resultado.valor_liquido:,.2f}** |

            ---

            **Codigo DARF:** {resultado.codigo_darf}

            **Data Limite Recolhimento:** {resultado.data_recolhimento.strftime('%d/%m/%Y')}

            {"**DISPENSA DE RETENCAO:** " + resultado.motivo_dispensa if resultado.dispensa_retencao else ""}
            """)

# Rodape
st.markdown("---")
st.markdown(
    "<small>Calculadora baseada na IN RFB 1.234/2012. "
    "Atualizacoes: IN RFB 2.145/2023 e IN RFB 2.239/2024.</small>",
    unsafe_allow_html=True
)
