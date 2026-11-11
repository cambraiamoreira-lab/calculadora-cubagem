import streamlit as st
import math
from datetime import datetime

# ============================================
# 🎨 CONFIGURAÇÃO E DESIGN
# ============================================
st.set_page_config(
    page_title="Calculadora de Frete",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Moderno
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    h1 {
        color: #2d3748;
        font-weight: 800;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        width: 100%;
    }
    .resultado-box {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    .volume-card {
        background: #f7fafc;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4299e1;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
#  TÍTULO
# ============================================
st.markdown('<h1>📦 Calculadora de Chargeable Weight</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #718096;">Frete Aéreo, Marítimo e Rodoviário</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================
# 🔧 SIDEBAR - CONFIGURAÇÕES
# ============================================
st.sidebar.header("⚙️ Configurações")

# Seleção do Modal
modal = st.sidebar.radio(
    "Modal de Transporte",
    ["✈️ Aéreo (IATA)", "🚢 Marítimo LCL", "🚢 Marítimo FCL", " Rodoviário/Expresso"],
    index=0
)

# Divisor Customizável
st.sidebar.markdown("---")
st.sidebar.subheader("📐 Divisor")

if "Aéreo" in modal:
    divisor_default = 6000
    info_divisor = "Padrão IATA: 6000 cm³/kg"
elif "LCL" in modal:
    divisor_default = 1000
    info_divisor = "1 CBM = 1000 kg (W/M)"
elif "FCL" in modal:
    divisor_default = 6000
    info_divisor = "Apenas para referência"
else:  # Rodoviário
    divisor_default = 5000
    info_divisor = "Comum: 5000 ou 6000"

divisor = st.sidebar.number_input(
    "Divisor (cm³/kg)",
    value=divisor_default,
    min_value=1000,
    max_value=10000,
    step=100,
    help=info_divisor
)

# ============================================
# 📊 GERENCIAMENTO DE VOLUMES (SESSION STATE)
# ============================================
if 'volumes' not in st.session_state:
    st.session_state.volumes = []

def adicionar_volume(comp, larg, alt, peso, qtd):
    st.session_state.volumes.append({
        'id': len(st.session_state.volumes) + 1,
        'comprimento': comp,
        'largura': larg,
        'altura': alt,
        'peso': peso,
        'quantidade': qtd
    })

def remover_volume(id_vol):
    st.session_state.volumes = [v for v in st.session_state.volumes if v['id'] != id_vol]

def limpar_volumes():
    st.session_state.volumes = []

# ============================================
# 📥 INPUT DE NOVOS VOLUMES
# ============================================
st.markdown("###  Adicionar Volume")

col1, col2 = st.columns([2, 1])

with col1:
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        comp = st.number_input("Comprimento (cm)", min_value=0.0, step=0.1, key="input_comp")
    with col_b:
        larg = st.number_input("Largura (cm)", min_value=0.0, step=0.1, key="input_larg")
    with col_c:
        alt = st.number_input("Altura (cm)", min_value=0.0, step=0.1, key="input_alt")
    
    col_d, col_e = st.columns(2)
    with col_d:
        peso = st.number_input("Peso Real (kg)", min_value=0.0, step=0.1, key="input_peso")
    with col_e:
        qtd = st.number_input("Qtd", min_value=1, value=1, step=1, key="input_qtd")

with col2:
    st.write("")  # Espaçamento
    st.write("")  # Espaçamento
    if st.button("➕ Adicionar", use_container_width=True):
        if comp > 0 and larg > 0 and alt > 0 and peso >= 0:
            adicionar_volume(comp, larg, alt, peso, qtd)
            st.success("Volume adicionado!")
        else:
            st.error("Preencha todas as dimensões!")

# ============================================
# 📋 LISTA DE VOLUMES ADICIONADOS
# ============================================
if st.session_state.volumes:
    st.markdown("---")
    st.markdown(f"### 📦 Volumes Adicionados ({len(st.session_state.volumes)})")
    
    for vol in st.session_state.volumes:
        cbm_vol = (vol['comprimento'] * vol['largura'] * vol['altura']) / 1000000
        st.markdown(f"""
        <div class="volume-card">
            <strong>Volume #{vol['id']}</strong> | 
            {vol['comprimento']}x{vol['largura']}x{vol['altura']} cm | 
            {vol['peso']} kg | Qtd: {vol['quantidade']} | 
            CBM: {cbm_vol * vol['quantidade']:.4f} m³
            <button onclick="remover({vol['id']})" style="float:right; background:#fc8181; color:white; border:none; padding:0.2rem 0.5rem; border-radius:5px; cursor:pointer;">×</button>
        </div>
        """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("️ Limpar Todos", use_container_width=True):
            limpar_volumes()
            st.rerun()
    with col_btn2:
        if st.button("🔢 Calcular Frete", use_container_width=True, type="primary"):
            st.session_state.calcular = True

# ============================================
# 🧮 CÁLCULOS
# ============================================
if st.session_state.volumes and st.session_state.get('calcular', False):
    st.markdown("---")
    st.markdown("###  Resultados")
    
    # Calcular totais
    peso_real_total = sum(v['peso'] * v['quantidade'] for v in st.session_state.volumes)
    cbm_total = sum((v['comprimento'] * v['largura'] * v['altura'] / 1000000) * v['quantidade'] 
                    for v in st.session_state.volumes)
    
    # Peso volumétrico
    if "Aéreo" in modal or "Rodoviário" in modal:
        peso_vol_total = sum((v['comprimento'] * v['largura'] * v['altura'] / divisor) * v['quantidade'] 
                            for v in st.session_state.volumes)
        peso_taxavel = max(peso_real_total, peso_vol_total)
        
        # Arredondamento para aéreo
        if "Aéreo" in modal:
            peso_taxavel = math.ceil(peso_taxavel * 2) / 2
        
        st.markdown(f"""
        <div class="resultado-box">
            <h2 style="color:white; margin:0;">Peso Taxável</h2>
            <h1 style="color:white; margin:0.5rem 0;">{peso_taxavel:.1f} kg</h1>
            <p style="color:white; margin:0; font-size:0.9rem;">
                (Base: {'Real' if peso_real_total >= peso_vol_total else 'Volumétrico'})
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Peso Real Total", f"{peso_real_total:.2f} kg")
            st.metric("Peso Volumétrico", f"{peso_vol_total:.2f} kg")
        with col2:
            st.metric("CBM Total", f"{cbm_total:.4f} m³")
            st.metric("Fator de Cubagem", f"{peso_vol_total/peso_real_total:.2f}" if peso_real_total > 0 else "0")
    
    elif "LCL" in modal:
        peso_toneladas = peso_real_total / 1000
        revenue_ton = max(peso_toneladas, cbm_total)
        
        st.markdown(f"""
        <div class="resultado-box">
            <h2 style="color:white; margin:0;">Revenue Ton (W/M)</h2>
            <h1 style="color:white; margin:0.5rem 0;">{revenue_ton:.3f}</h1>
            <p style="color:white; margin:0; font-size:0.9rem;">
                (Base: {'Peso' if peso_toneladas >= cbm_total else 'Cubagem'})
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Peso Total", f"{peso_real_total:.2f} kg")
        with col2:
            st.metric("Peso em Toneladas", f"{peso_toneladas:.3f} t")
        with col3:
            st.metric("CBM Total", f"{cbm_total:.4f} m³")
        
        st.info(f"💡 **Regra W/M:** O frete será cobrado sobre {revenue_ton:.3f} (maior entre {peso_toneladas:.3f}t e {cbm_total:.4f} CBM)")
    
    elif "FCL" in modal:
        st.success(f"✅ **CBM Total:** {cbm_total:.4f} m³")
        st.info("ℹ️ **FCL:** Cobrado por container. Use o CBM para verificar se cabe no container escolhido.")
        
        # Capacidade de containers
        containers = {
            "20 pés": 33,
            "40 pés": 67,
            "40 pés High Cube": 76
        }
        
        st.markdown("#### 📦 Capacidade de Containers:")
        for tipo, capacidade in containers.items():
            cabe = "✅ Cabe" if cbm_total <= capacidade else "❌ Não cabe"
            st.write(f"{cabe} - Container {tipo} ({capacidade} m³)")
    
    # ============================================
    # 📱 RESUMO PARA WHATSAPP
    # ============================================
    st.markdown("---")
    st.markdown("### 📱 Resumo para Cliente")
    
    if "Aéreo" in modal:
        texto_resumo = f"""
*COTAÇÃO DE FRETE - AÉREO*

📦 *Volume:* {len(st.session_state.volumes)} volume(s)
📏 *Dimensões:* {cbm_total:.3f} m³
⚖️ *Peso Real:* {peso_real_total:.1f} kg
📐 *Peso Volumétrico:* {peso_vol_total:.1f} kg
💰 *Peso Taxável:* {peso_taxavel:.1f} kg

*Base de cálculo:* {'Peso Real' if peso_real_total >= peso_vol_total else 'Peso Volumétrico'}
"""
    elif "LCL" in modal:
        texto_resumo = f"""
*COTAÇÃO DE FRETE - MARÍTIMO LCL*

📦 *Volume:* {len(st.session_state.volumes)} volume(s)
📏 *CBM Total:* {cbm_total:.3f} m³
⚖️ *Peso:* {peso_real_total:.1f} kg ({peso_toneladas:.3f} t)
💰 *Revenue Ton (W/M):* {revenue_ton:.3f}

*Base de cálculo:* {'Peso' if peso_toneladas >= cbm_total else 'Cubagem'}
"""
    else:
        texto_resumo = f"""
*COTAÇÃO DE FRETE*

📦 *Volume:* {len(st.session_state.volumes)} volume(s)
 *CBM Total:* {cbm_total:.3f} m³
⚖️ *Peso:* {peso_real_total:.1f} kg
"""
    
    st.text_area("Copie e cole no WhatsApp:", value=texto_resumo, height=200)
    
    # Botão para recomeçar
    if st.button("🔄 Nova Cotação"):
        limpar_volumes()
        st.session_state.calcular = False
        st.rerun()

# ============================================
# 💡 RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; padding: 1rem;">
    <p><strong>💡 Dica:</strong> Adicione todos os volumes antes de calcular.</p>
    <p>Calculadora desenvolvida para profissionais de Comércio Exterior</p>
</div>
""", unsafe_allow_html=True)
