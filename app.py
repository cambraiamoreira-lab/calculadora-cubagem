import streamlit as st
import math
import streamlit.components.v1 as components

# ============================================
# 🎨 CONFIGURAÇÃO E DESIGN (CORES MBX CARGO)
# ============================================
st.set_page_config(
    page_title="MBX Cargo - Calculadora de Frete",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed" # Começa fechada para focar no modal
)

# Cores da Marca
COR_LARANJA = "#F39C12"
COR_AZUL_MARINHO = "#1A252F"
COR_CINZA = "#95A5A6"
COR_FUNDO = "#F4F6F7"

st.markdown(f"""
<style>
    /* Fundo Geral */
    .stApp {{
        background-color: {COR_FUNDO};
    }}
    
    /* Container Principal */
    .main .block-container {{
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        max-width: 800px;
        margin: 0 auto;
    }}
    
    /* Títulos */
    h1, h2, h3 {{
        color: {COR_AZUL_MARINHO};
        font-weight: 700;
    }}
    
    /* Botões Principais */
    .stButton>button {{
        background: {COR_LARANJA};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background: #d68910;
        transform: translateY(-2px);
    }}
    
    /* Cards de Volume */
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
    
    /* Resultado Box */
    .resultado-box {{
        background: {COR_AZUL_MARINHO};
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(26, 37, 47, 0.3);
    }}
    .resultado-box h1 {{
        color: {COR_LARANJA};
        font-size: 3rem;
        margin: 0;
    }}
    .resultado-box p {{
        color: white;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }}

    /* Modal Overlay (Escondido por padrão) */
    #modal-overlay {{
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(26, 37, 47, 0.95);
        z-index: 9999;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }}
    .modal-content {{
        background: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        max-width: 90%;
        width: 400px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}
    .modal-btn {{
        display: block;
        width: 100%;
        padding: 1rem;
        margin: 10px 0;
        background: {COR_AZUL_MARINHO};
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }}
    .modal-btn:hover {{
        background: {COR_LARANJA};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# 🧠 LÓGICA DO MODAL AUTOMÁTICO (JAVASCRIPT)
# ============================================
# Este script faz o modal aparecer após 5 segundos e fecha ao clicar
js_modal = """
<script>
    // Espera 5 segundos (5000ms) e mostra o modal
    setTimeout(function() {
        document.getElementById('modal-overlay').style.display = 'flex';
    }, 5000);

    // Função para fechar o modal e "clicar" no botão invisível do Streamlit
    function escolherModal(tipo) {
        document.getElementById('modal-overlay').style.display = 'none';
        // Encontra o botão invisível correspondente e clica nele
        document.getElementById('btn-' + tipo).click();
    }
</script>

<div id="modal-overlay">
    <div class="modal-content">
        <h2 style="color: #1A252F; margin-bottom: 2rem;">Bem-vindo à MBX Cargo</h2>
        <p style="color: #7f8c8d; margin-bottom: 2rem;">Selecione o modal para iniciar:</p>
        
        <button class="modal-btn" onclick="escolherModal('aereo')">✈️ AÉREO</button>
        <button class="modal-btn" onclick="escolherModal('lcl')">🚢 MARÍTIMO LCL</button>
        <button class="modal-btn" onclick="escolherModal('fcl')">🚢 MARÍTIMO FCL</button>
        <button class="modal-btn" onclick="escolherModal('rod')">🚚 RODOVIÁRIO</button>
    </div>
</div>
"""
components.html(js_modal, height=0, width=0) # Injeta o script sem ocupar espaço

# ============================================
# 🕵️ BOTÕES INVISÍVEIS (PARA O JS CLICAR)
# ============================================
# Estes botões ficam escondidos e só servem para o JS ativar o modal escolhido
col_hidden = st.columns(4)
with col_hidden[0]:
    if st.button("aereo", key="btn-aereo", style="display:none"): # Nota: Streamlit não aceita style display none direto assim, vamos usar um truque
        st.session_state.modal_escolhido = "Aéreo"
with col_hidden[1]:
    if st.button("lcl", key="btn-lcl"):
        st.session_state.modal_escolhido = "Marítimo LCL"
with col_hidden[2]:
    if st.button("fcl", key="btn-fcl"):
        st.session_state.modal_escolhido = "Marítimo FCL"
with col_hidden[3]:
    if st.button("rod", key="btn-rod"):
        st.session_state.modal_escolhido = "Rodoviário"

# Esconder os botões via CSS (truque)
st.markdown("""
<style>
    #btn-aereo, #btn-lcl, #btn-fcl, #btn-rod { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Inicializa o state
if 'modal_escolhido' not in st.session_state:
    st.session_state.modal_escolhido = None

# ============================================
# 📱 TELA PRINCIPAL
# ============================================
if st.session_state.modal_escolhido is None:
    # Tela de espera (antes dos 5 segundos)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.image("logo.png", width=250) # Certifique-se que subiu a logo como logo.png
    st.markdown("<h1 style='text-align:center; color:#1A252F;'>MBX CARGO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#7f8c8d;'>Carregando calculadora...</p>", unsafe_allow_html=True)
    
    # Barra de progresso animada (fake)
    st.progress(0)
    
else:
    # APP CARREGADO
    modal = st.session_state.modal_escolhido
    
    # Cabeçalho
    col_logo, col_titulo = st.columns([1, 3])
    with col_logo:
        st.image("logo.png", width=100)
    with col_titulo:
        st.title(f"Calculadora {modal}")
        st.caption("Sistema de Cubagem Inteligente")
    
    st.markdown("---")
    
    # Configurações do Modal
    if modal == "Aéreo":
        divisor = 6000
        tipo_calc = "Peso Taxável (kg)"
    elif modal == "Marítimo LCL":
        divisor = 1000 # 1 CBM = 1000kg
        tipo_calc = "Revenue Ton (W/M)"
    elif modal == "Rodoviário":
        divisor = st.number_input("Divisor (geralmente 3000 ou 5000)", value=3000)
        tipo_calc = "Peso Taxável (kg)"
    else: # FCL
        divisor = 6000
        tipo_calc = "CBM Total"

    # ============================================
    # 📦 GESTÃO DE MÚLTIPLOS VOLUMES
    # ============================================
    st.subheader("📦 Adicionar Volumes")
    st.caption("Adicione quantas caixas forem necessárias com dimensões diferentes.")
    
    # Formulário de entrada
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
            qtd = st.number_input("Quantidade de Caixas", min_value=1, value=1, step=1)
        
        submitted = st.form_submit_button("➕ Adicionar à Lista", use_container_width=True)
        
        if submitted:
            if 'lista_volumes' not in st.session_state:
                st.session_state.lista_volumes = []
            
            st.session_state.lista_volumes.append({
                'comp': comp, 'larg': larg, 'alt': alt,
                'peso': peso, 'qtd': qtd
            })
            st.success(f"Adicionado: {qtd}x caixa(s) de {comp}x{larg}x{alt}cm")

    # ============================================
    # 📋 LISTA DE VOLUMES (Tabela Visual)
    # ============================================
    if 'lista_volumes' in st.session_state and len(st.session_state.lista_volumes) > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Cargas Adicionadas")
        
        for i, vol in enumerate(st.session_state.lista_volumes):
            cbm_un = (vol['comp'] * vol['larg'] * vol['alt']) / 1000000
            st.markdown(f"""
            <div class="volume-card">
                <div>
                    <strong>Volume {i+1}:</strong> {vol['qtd']}x caixa(s)<br>
                    <small style="color:#7f8c8d;">{vol['comp']}x{vol['larg']}x{vol['alt']} cm | {vol['peso']} kg cada</small>
                </div>
                <div style="text-align:right;">
                    <strong>{cbm_un * vol['qtd']:.3f} m³</strong><br>
                    <small style="color:#e74c3c; cursor:pointer;" onclick="alert('Função de remover em desenvolvimento')">Remover</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Botões de Ação
        col_calc, col_clear = st.columns(2)
        with col_calc:
            calcular = st.button("🧮 CALCULAR FRETE", type="primary", use_container_width=True)
        with col_clear:
            if st.button("🗑️ Limpar Tudo", use_container_width=True):
                st.session_state.lista_volumes = []
                st.rerun()
        
        # ============================================
        # 🎯 RESULTADOS
        # ============================================
        if calcular:
            st.markdown("---")
            
            # Totais
            peso_real_total = sum(v['peso'] * v['qtd'] for v in st.session_state.lista_volumes)
            cbm_total = sum((v['comp'] * v['larg'] * v['alt'] / 1000000) * v['qtd'] for v in st.session_state.lista_volumes)
            peso_vol_total = sum((v['comp'] * v['larg'] * v['alt'] / divisor) * v['qtd'] for v in st.session_state.lista_volumes)
            
            if modal in ["Aéreo", "Rodoviário"]:
                peso_taxavel = max(peso_real_total, peso_vol_total)
                if modal == "Aéreo":
                    peso_taxavel = math.ceil(peso_taxavel * 2) / 2 # Arredonda 0.5
                
                st.markdown(f"""
                <div class="resultado-box">
                    <p>{tipo_calc}</p>
                    <h1>{peso_taxavel:.1f} kg</h1>
                    <p style="font-size:0.9rem; opacity:0.8;">Base: {'Real' if peso_real_total >= peso_vol_total else 'Volumétrico'}</p>
                </div>
                """, unsafe_allow_html=True)
                
            elif modal == "Marítimo LCL":
                peso_ton = peso_real_total / 1000
                revenue_ton = max(peso_ton, cbm_total)
                
                st.markdown(f"""
                <div class="resultado-box">
                    <p>{tipo_calc}</p>
                    <h1>{revenue_ton:.3f}</h1>
                    <p style="font-size:0.9rem; opacity:0.8;">Base: {'Peso' if peso_ton >= cbm_total else 'Cubagem'}</p>
                </div>
                """, unsafe_allow_html=True)
            
            elif modal == "Marítimo FCL":
                st.markdown(f"""
                <div class="resultado-box">
                    <p>Volume Total da Carga</p>
                    <h1>{cbm_total:.2f} m³</h1>
                    <p style="font-size:0.9rem; opacity:0.8;">Verifique a capacidade do container</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Dica de Container
                if cbm_total <= 28:
                    st.info("✅ Cabe em um Container 20 pés (aprox. 28-33m³)")
                elif cbm_total <= 58:
                    st.info("✅ Cabe em um Container 40 pés (aprox. 58-67m³)")
                else:
                    st.warning("⚠️ Necessário mais de um container ou 40' HC")

            # ============================================
            # 📱 RESUMO WHATSAPP
            # ============================================
            st.markdown("---")
            st.subheader("📱 Enviar para Cliente")
            
            texto = f"*MBX CARGO - Cotação {modal}*\n\n"
            texto += f"📦 *Volumes:* {len(st.session_state.lista_volumes)} tipos\n"
            texto += f"📏 *CBM Total:* {cbm_total:.3f} m³\n"
            texto += f"⚖️ *Peso Real:* {peso_real_total:.1f} kg\n"
            
            if modal in ["Aéreo", "Rodoviário"]:
                texto += f"💰 *Peso Taxável:* {peso_taxavel:.1f} kg\n"
            elif modal == "LCL":
                texto += f"💰 *Revenue Ton:* {revenue_ton:.3f}\n"
            
            st.text_area("Copie abaixo:", value=texto, height=150)
            
            if st.button("🔄 Nova Cotação"):
                st.session_state.lista_volumes = []
                st.session_state.modal_escolhido = None # Volta para o modal inicial
                st.rerun()

    else:
        st.info("👆 Use o formulário acima para adicionar o primeiro volume.")

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align:center; color:#95A5A6; font-size:0.8rem;'>MBX Cargo © 2026 - Todos os direitos reservados</p>", unsafe_allow_html=True)
