import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(page_title="Calculadora de Cubagem Pro", page_icon="📦", layout="wide")

# --- Inicialização do Estado da Sessão ---
# Usado para permitir limpar os dados inseridos
if "data_editor_key" not in st.session_state:
    st.session_state.data_editor_key = 0

def limpar_campos():
    """Incrementa a chave do data_editor para forçar a recriação da tabela vazia."""
    st.session_state.data_editor_key += 1

# --- Cabeçalho e Instruções ---
st.title("📦 Calculadora de Cubagem Logística")
st.markdown("""
Calcule o peso cubado e o peso taxável da sua carga de forma rápida e precisa. 
Adicione os volumes na tabela abaixo para calcular múltiplos itens de uma só vez.
""")

# Instruções escondidas em um expander para não poluir a tela inicial
with st.expander("ℹ️ Como usar esta calculadora?"):
    st.write("""
    1. **Insira as dimensões** de cada volume (em centímetros) e o **Peso Real** (em kg).
    2. Você pode adicionar quantas linhas precisar clicando no ícone de **+** no final da tabela.
    3. **Selecione o Fator de Cubagem** adequado à sua transportadora.
    4. O sistema calculará automaticamente o **Peso Cubado** e definirá o **Peso Taxável** (o maior entre o real e o cubado).
    """)

# --- Configuração do Fator de Cubagem ---
st.subheader("1. Configuração da Transportadora")
col_fator, col_info = st.columns([1, 2])

with col_fator:
    # Selectbox com os fatores mais comuns, trazendo clareza
    fator_cubagem = st.selectbox(
        "Fator de Cubagem (Divisor)",
        options=[6000, 5000, 3000],
        index=0,
        help="O divisor padrão do mercado brasileiro é 6000. Transportadoras aéreas e expressas costumam usar 5000 ou 3000."
    )

with col_info:
    st.info(f"**Fórmula aplicada:** Peso Cubado = (Comprimento × Largura × Altura) ÷ {fator_cubagem}")

st.divider()

# --- Entrada de Dados (Múltiplos Itens) ---
st.subheader("2. Dados dos Volumes")

# Criando um DataFrame inicial vazio com as colunas necessárias
df_inicial = pd.DataFrame({
    "Descrição do Item": ["Caixa 1", "", ""],
    "Comprimento (cm)": [0.0, 0.0, 0.0],
    "Largura (cm)": [0.0, 0.0, 0.0],
    "Altura (cm)": [0.0, 0.0, 0.0],
    "Peso Real (kg)": [0.0, 0.0, 0.0]
})

# Usando o st.data_editor para permitir múltiplas linhas
# O column_config previne erros: impede números negativos
edited_df = st.data_editor(
    df_inicial,
    num_rows="dynamic",
    key=f"editor_{st.session_state.data_editor_key}",
    column_config={
        "Descrição do Item": st.column_config.TextColumn("Descrição do Item", required=True),
        "Comprimento (cm)": st.column_config.NumberColumn("Comprimento (cm)", min_value=0.0, format="%.2f", required=True),
        "Largura (cm)": st.column_config.NumberColumn("Largura (cm)", min_value=0.0, format="%.2f", required=True),
        "Altura (cm)": st.column_config.NumberColumn("Altura (cm)", min_value=0.0, format="%.2f", required=True),
        "Peso Real (kg)": st.column_config.NumberColumn("Peso Real (kg)", min_value=0.0, format="%.2f", required=True),
    },
    use_container_width=True
)

st.divider()

# --- Cálculos e Resultados ---
# Filtra apenas as linhas onde as dimensões e o peso foram preenchidos (> 0)
df_valido = edited_df[
    (edited_df["Comprimento (cm)"] > 0) & 
    (edited_df["Largura (cm)"] > 0) & 
    (edited_df["Altura (cm)"] > 0) & 
    (edited_df["Peso Real (kg)"] > 0)
].copy()

st.subheader("3. Resultados do Cálculo")

if df_valido.empty:
    st.warning("⚠️ Preencha as dimensões e o peso real na tabela acima para visualizar os resultados.")
else:
    # Realizando os cálculos
    # Volume em m³ = (C * L * A) / 1.000.000
    df_valido["Volume (m³)"] = (df_valido["Comprimento (cm)"] * df_valido["Largura (cm)"] * df_valido["Altura (cm)"]) / 1000000
    
    # Peso Cubado = (C * L * A) / Fator
    df_valido["Peso Cubado (kg)"] = (df_valido["Comprimento (cm)"] * df_valido["Largura (cm)"] * df_valido["Altura (cm)"]) / fator_cubagem
    
    # Peso Taxável = O maior valor entre o Peso Real e o Peso Cubado
    df_valido["Peso Taxável (kg)"] = df_valido[["Peso Real (kg)", "Peso Cubado (kg)"]].max(axis=1)
    
    # Formatação para exibição
    colunas_exibicao = ["Descrição do Item", "Volume (m³)", "Peso Real (kg)", "Peso Cubado (kg)", "Peso Taxável (kg)"]
    df_exibicao = df_valido[colunas_exibicao].round(2)
    
    # Exibição em container destacado
    with st.container(border=True):
        st.dataframe(
            df_exibicao,
            use_container_width=True,
            hide_index=True
        )
    
    # --- Resumo (KPIs) ---
    st.markdown("### 📊 Resumo da Carga")
    col1, col2, col3, col4 = st.columns(4)
    
    total_volumes = len(df_valido)
    total_volume_m3 = df_valido["Volume (m³)"].sum()
    total_peso_real = df_valido["Peso Real (kg)"].sum()
    total_peso_taxavel = df_valido["Peso Taxável (kg)"].sum()
    
    col1.metric("Total de Volumes", f"{total_volumes} un")
    col2.metric("Volume Total", f"{total_volume_m3:.3f} m³")
    col3.metric("Peso Real Total", f"{total_peso_real:.2f} kg")
    col4.metric("Peso Taxável Total", f"{total_peso_taxavel:.2f} kg", delta="Base para Frete", delta_color="off")

    # --- Exportação de Dados ---
    st.markdown("### 📥 Exportar Dados")
    csv = df_valido[colunas_exibicao].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar Relatório em CSV",
        data=csv,
        file_name="relatorio_cubagem.csv",
        mime="text/csv",
        type="primary"
    )

st.divider()

# --- Botão de Limpar ---
if st.button("🔄 Limpar Tabela e Recomeçar"):
    limpar_campos()
    st.rerun()