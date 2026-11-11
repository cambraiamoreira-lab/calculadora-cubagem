import streamlit as st
import math

# ============================================
# 🎨 CONFIGURAÇÃO
# ============================================
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
        display: flex;
        justify-content: space-between;
        align-items: center;
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

# ============================================
# 🧠 ESTADO INICIAL
# ============================================
if 'modal_escolhido' not in st.session_state:
    st.session_state.modal_escolhido = None
if 'lista_volumes' not in st.session_state:
    st.session_state.lista_volumes = []
if 'calculado' not in st.session_state:
    st.session_state.calculado = False

# ============================================
# 📱 TELA 1: SELEÇÃO DE MODAL
# ============================================
if st.session_state.modal_escolhido is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Tenta carregar a logo
    try:
        st.image("logo.png", width=200)
        st.markdown("<h1 style='text-align:center; color:#1A252F;'>MBX CARGO</h1>", unsafe_allow_html=True)
    except:
        st.markdown("<h1 style='text-align:center; color:#1A252F;'>📦 MBX CARGO</h1>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center; color:#7f8c8d; margin-bottom:3rem;'>Calculadora de Frete - Selecione o modal:</p>", unsafe_allow_html=True)
    
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
    
    # Cabeçalho com logo
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            st.image("logo.png", width=80)
        except:
            st.markdown("📦")
    with col2:
        st.title(f"MBX Cargo - {modal}")
    
    # Botão de voltar ao início
    if st.button("🏠 Voltar ao Início"):
        st.session_state.modal_escolhido = None
        st.session_state.lista_volumes = []
        st.session_state.calculado = False
        st.rerun()
    
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
            comp = st.number_input("Comprimento (cm)", min_value=0.1, step=0.1, key="comp")
        with col2:
            larg = st.number_input("Largura (cm)", min_value=0.1, step=0.1, key="larg")
        with col3:
            alt = st.number_input("Altura (cm)", min_value=0.1, step=0.1, key="alt")
        
        col4, col5 = st.columns(2)
        with col4:
            peso = st.number_input("Peso Unitário (kg)", min_value=0.1, step=0.1, key="peso")
        with col5:
            qtd = st.number_input("Quantidade", min_value=1, value=1, step=1, key="qtd")
        
        submitted = st.form_submit_button("➕ Adicionar", use_container_width=True)
        
        if submitted:
            st.session_state.lista_volumes.append({
                'comp': comp, 'larg': larg, 'alt': alt,
                'peso': peso, 'qtd': qtd
            })
            st.session_state.calculado = False  # Reseta cálculo ao adicionar novo volume
            st.success(f"✅ Adicionado: {qtd}x caixa(s) {comp}x{larg}x{alt}cm")
            st.rerun()
    
    # ============================================
    # 📋 LISTA DE VOLUMES COM BOTÃO REMOVER
    # ============================================
    if st.session_state.lista_volumes:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(f"📋 Volumes Adicionados ({len(st.session_state.lista_volumes)})")
        
        for i, vol in enumerate(st.session_state.lista_volumes):
            cbm_un = (vol['comp'] * vol['larg'] * vol['alt']) / 1000000
            
            col_card, col_btn = st.columns([4, 1])
            with col_card:
                st.markdown(f"""
                <div class="volume-card">
                    <div>
                        <strong>Volume {i+1}:</strong> {vol['qtd']}x caixa(s)<br>
                        <small style="color:#7f8c8d;">{vol['comp']}x{vol['larg']}x{vol['alt']} cm | {vol['peso']} kg cada</small>
                    </div>
                    <div style="text-align:right;">
                        <strong>{cbm_un * vol['qtd']:.3f} m³</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if st.button(f"❌", key=f"rem_{i}", help=f"Remover volume {i+1}"):
                    st.session_state.lista_volumes.pop(i)
                    st.session_state.calculado = False
                    st.rerun()
        
        # Botões de Ação
        st.markdown("---")
        col_calc, col_clear = st.columns(2)
        with col_calc:
            if st.button("🧮 CALCULAR FRETE", type="primary", use_container_width=True):
                st.session_state.calculado = True
                st.rerun()
        with col_clear:
            if st.button("🗑️ Limpar Tudo", use_container_width=True):
                st.session_state.lista_volumes = []
                st.session_state.calculado = False
                st.rerun()
        
        # ============================================
        # 🎯 RESULTADOS (aparece após calcular)
        # ============================================
        if st.session_state.calculado:
            st.markdown("---")
            st.subheader("🎯 Resultado do Cálculo")
            
            # Cálculos
            peso_real_total = sum(v['peso'] * v['qtd'] for v in st.session_state.lista_volumes)
            cbm_total = sum((v['comp'] * v['larg'] * v['alt'] / 1000000) * v['qtd'] for v in st.session_state.lista_volumes)
            peso_vol_total = sum((v['comp'] * v['larg'] * v['alt'] / divisor) * v['qtd'] for v in st.session_state.lista_volumes)
            
            if modal in ["Aéreo", "Rodoviário"]:
                peso_taxavel = max(peso_real_total, peso_vol_total)
                if modal == "Aéreo":
                    peso_taxavel = math.ceil(peso_taxavel * 2) / 2
                
                st.markdown(f"""
                <div class="resultado-box">
                    <p style="font-size:1.2rem; margin:0;">{tipo_calc}</p>
                    <h1>{peso_taxavel:.1f} kg</h1>
                    <p style="font-size:0.9rem; opacity:0.8;">Base: {'Peso Real' if peso_real_total >= peso_vol_total else 'Peso Volumétrico'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Peso Real Total", f"{peso_real_total:.2f} kg")
                    st.metric("Peso Volumétrico", f"{peso_vol_total:.2f} kg")
                with col2:
                    st.metric("CBM Total", f"{cbm_total:.4f} m³")
                    st.metric("Divisor Usado", f"{divisor}")
                
            elif modal == "Marítimo LCL":
                peso_ton = peso_real_total / 1000
                revenue_ton = max(peso_ton, cbm_total)
                
                st.markdown(f"""
                <div class="resultado-box">
                    <p style="font-size:1.2rem; margin:0;">{tipo_calc}</p>
                    <h1>{revenue_ton:.3f}</h1>
                    <p style="font-size:0.9rem; opacity:0.8;">Base: {'Peso' if peso_ton >= cbm_total else 'Cubagem'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Peso Total", f"{peso_real_total:.2f} kg")
                with col2:
                    st.metric("Peso em Toneladas", f"{peso_ton:.3f} t")
                with col3:
                    st.metric("CBM Total", f"{cbm_total:.4f} m³")
                
                st.info(f"💡 **Regra W/M:** O frete será cobrado sobre {revenue_ton:.3f} (maior entre {peso_ton:.3f}t e {cbm_total:.4f} CBM)")
            
            elif modal == "Marítimo FCL":
                st.markdown(f"""
                <div class="resultado-box">
                    <p style="font-size:1.2rem; margin:0;">Volume Total da Carga</p>
                    <h1>{cbm_total:.2f} m³</h1>
                </div>
                """, unsafe_allow_html=True)
                
                if cbm_total <= 28:
                    st.success("✅ Cabe em Container 20 pés (aprox. 28-33m³)")
                elif cbm_total <= 58:
                    st.success("✅ Cabe em Container 40 pés (aprox. 58-67m³)")
                elif cbm_total <= 76:
                    st.info("⚠️ Cabe em Container 40' High Cube (aprox. 76m³)")
                else:
                    st.warning(f"⚠️ Necessário mais de um container. Total: {cbm_total:.2f} m³")
            
            # ============================================
            # 📱 RESUMO WHATSAPP
            # ============================================
            st.markdown("---")
            st.subheader("📱 Resumo para Cliente (WhatsApp)")
            
            if modal == "Aéreo":
                texto = f"*MBX CARGO - Cotação AÉREA*\n\n"
                texto += f"📦 *Volumes:* {len(st.session_state.lista_volumes)} tipo(s)\n"
                texto += f"📏 *CBM Total:* {cbm_total:.3f} m³\n"
                texto += f"⚖️ *Peso Real:* {peso_real_total:.1f} kg\n"
                texto += f"📐 *Peso Volumétrico:* {peso_vol_total:.1f} kg\n"
                texto += f"💰 *Peso Taxável:* {peso_taxavel:.1f} kg\n\n"
                texto += f"_Base de cálculo: {'Peso Real' if peso_real_total >= peso_vol_total else 'Peso Volumétrico'}_"
            elif modal == "Marítimo LCL":
                texto = f"*MBX CARGO - Cotação MARÍTIMA LCL*\n\n"
                texto += f"📦 *Volumes:* {len(st.session_state.lista_volumes)} tipo(s)\n"
                texto += f"📏 *CBM Total:* {cbm_total:.3f} m³\n"
                texto += f"⚖️ *Peso:* {peso_real_total:.1f} kg ({peso_ton:.3f} t)\n"
                texto += f"💰 *Revenue Ton (W/M):* {revenue_ton:.3f}\n\n"
                texto += f"_Base de cálculo: {'Peso' if peso_ton >= cbm_total else 'Cubagem'}_"
            elif modal == "Marítimo FCL":
                texto = f"*MBX CARGO - Cotação MARÍTIMA FCL*\n\n"
                texto += f"📦 *Volumes:* {len(st.session_state.lista_volumes)} tipo(s)\n"
                texto += f"📏 *CBM Total:* {cbm_total:.3f} m³\n"
                texto += f"⚖️ *Peso:* {peso_real_total:.1f} kg\n\n"
                if cbm_total <= 28:
                    texto += "✅ *Container sugerido:* 20 pés"
                elif cbm_total <= 58:
                    texto += "✅ *Container sugerido:* 40 pés"
                else:
                    texto += "⚠️ *Container sugerido:* 40' HC ou múltiplos"
            else:  # Rodoviário
                texto = f"*MBX CARGO - Cotação RODOVIÁRIA*\n\n"
                texto += f"📦 *Volumes:* {len(st.session_state.lista_volumes)} tipo(s)\n"
                texto += f"📏 *CBM Total:* {cbm_total:.3f} m³\n"
                texto += f"⚖️ *Peso Real:* {peso_real_total:.1f} kg\n"
                texto += f"📐 *Peso Volumétrico:* {peso_vol_total:.1f} kg\n"
                texto += f"💰 *Peso Taxável:* {peso_taxavel:.1f} kg\n"
                texto += f"_Divisor usado: {divisor}_"
            
            st.text_area("Copie o texto abaixo e cole no WhatsApp:", value=texto, height=200)
            
            st.markdown("---")
            st.markdown("### 🔄 Opções")
            col_nova, col_voltar = st.columns(2)
            with col_nova:
                if st.button("🔄 Nova Cotação (mesmo modal)", use_container_width=True):
                    st.session_state.lista_volumes = []
                    st.session_state.calculado = False
                    st.rerun()
            with col_voltar:
                if st.button("🏠 Trocar de Modal", use_container_width=True):
                    st.session_state.modal_escolhido = None
                    st.session_state.lista_volumes = []
                    st.session_state.calculado = False
                    st.rerun()
    
    else:
        st.info("👆 Adicione o primeiro volume usando o formulário acima.")

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align:center; color:#95A5A6; font-size:0.8rem;'>MBX Cargo © 2026 - Todos os direitos reservados</p>", unsafe_allow_html=True)