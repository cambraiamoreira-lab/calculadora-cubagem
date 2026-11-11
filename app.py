import streamlit as st
import math

st.set_page_config(
    page_title="MBX Cargo - Calculadora de Frete",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

COR_LARANJA = "#F39C12"
COR_AZUL_MARINHO = "#1A252F"

st.markdown(f"""
<style>
    .stApp {{ background-color: #F4F6F7; }}
    .main .block-container {{
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        max-width: 800px;
        margin: 0 auto;
    }}
    h1, h2, h3 {{ color: {COR_AZUL_MARINHO}; font-weight: 700; }}
    .stButton>button {{
        background: {COR_LARANJA};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
    }}
    .volume-card {{
        background: white;
        border-left: 5px solid {COR_LARANJA};
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .resultado-box {{
        background: {COR_AZUL_MARINHO};
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }}
    .resultado-box h1 {{
        color: {COR_LARANJA};
        font-size: 3rem;
        margin: 0;
    }}
</style>
""", unsafe_allow_html=True)

if 'modal_escolhido' not in st.session_state:
    st.session_state.modal_escolhido = None
if 'lista_volumes' not in st.session_state:
    st.session_state.lista_volumes = []
# ============================================
# 📱 TELA 1: SELEÇÃO DE MODAL
# ============================================
if st.session_state.modal_escolhido is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    try:
        st.image("logo.png", width=200)
    except:
        st.markdown("<h1 style='text-align:center;'>📦 MBX CARGO</h1>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; color:#1A252F;'>Calculadora de Frete</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#7f8c8d; margin-bottom:3rem;'>Selecione o modal de transporte:</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✈️ AÉREO", use_container_width=True):
            st.session_state.modal_escolhido = "Aéreo"
            st.rerun()
        if st.button("🚢 MARÍTIMO LCL", use_container_width=True):
            st.session_state.modal_escolhido = "Marítimo LCL"
            st.rerun()
    with col2:
        if st.button("🚢 MARÍTIMO FCL", use_container_width=True):
            st.session_state.modal_escolhido = "Marítimo FCL"
            st.rerun()
        if st.button("🚚 RODOVIÁRIO", use_container_width=True):
            st.session_state.modal_escolhido = "Rodoviário"
            st.rerun()
# ============================================
# 📱 TELA 2: CALCULADORA
# ============================================
else:
    modal = st.session_state.modal_escolhido
    
    # Cabeçalho
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            st.image("logo.png", width=80)
        except:
            st.markdown("📦")
    with col2:
        st.title(f"MBX Cargo - {modal}")
    
    st.markdown("---")
    
    # Configurações do Modal
    if modal == "Aéreo":
        divisor = 6000
        tipo_calc = "Peso Taxável (kg)"
    elif modal == "Marítimo LCL":
        divisor = 1000
        tipo_calc = "Revenue Ton (W/M)"
    elif modal == "Rodoviário":
        divisor = st.number_input("Divisor (geralmente 3000 ou 5000)", value=3000, step=100)
        tipo_calc = "Peso Taxável (kg)"
    else:
        divisor = 6000
        tipo_calc = "CBM Total"
    
    # ============================================
    # 📦 FORMULÁRIO DE VOLUMES
    # ============================================
    st.subheader("📦 Adicionar Volume")
    
    with st.form("form_volume", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            comp = st.number_input("Comprimento (cm)", min_value=0.1, step=0.1)
        with col2:
            larg = st.number_input("Largura (cm)", min_value=0.1, step=0.1)
        with col3:
            alt = st.number_input("Altura (cm)", min_value=0.1, step=0.1)
        
        col4, col5 = st.columns(2)
        with col4:
            peso = st.number_input("Peso Unitário (kg)", min_value=0.1, step=0.1)
        with col5:
            qtd = st.number_input("Quantidade", min_value=1, value=1, step=1)
        
        submitted = st.form_submit_button("➕ Adicionar", use_container_width=True)
        
        if submitted:
            st.session_state.lista_volumes.append({
                'comp': comp, 'larg': larg, 'alt': alt,
                'peso': peso, 'qtd': qtd
            })
            st.success(f"✅ Adicionado: {qtd}x caixa(s) {comp}x{larg}x{alt}cm")
    
    # ============================================
    # 📋 LISTA DE VOLUMES
    # ============================================
    if st.session_state.lista_volumes:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(f"📋 Volumes Adicionados ({len(st.session_state.lista_volumes)})")
        
        for i, vol in enumerate(st.session_state.lista_volumes):
            cbm_un = (vol['comp'] * vol['larg'] * vol['alt']) / 1000000
            st.markdown(f"""
            <div class="volume-card">
                <strong>Volume {i+1}:</strong> {vol['qtd']}x caixa(s) | 
                {vol['comp']}x{vol['larg']}x{vol['alt']} cm | 
                {vol['peso']} kg cada | 
                <strong>{cbm_un * vol['qtd']:.3f} m³</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Botões de Ação
        col_calc, col_clear = st.columns(2)
        with col_calc:
            calcular = st.button("🧮 CALCULAR", type="primary", use_container_width=True)
        with col_clear:
            if st.button("🗑️ Limpar Tudo", use_container_width=True):
                st.session_state.lista_volumes = []
                st.rerun()
