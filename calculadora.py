import streamlit as st

# 1. Configuração da página com o nome da empresa
st.set_page_config(
    page_title="MBX Cargo - Calculadora de Cubagem",
    page_icon="📦",
    layout="centered"
)

# 2. Exibindo a Logo da Empresa (Link Raw que preparamos)
url_logo = "https://raw.githubusercontent.com/cambraiamoreira-lab/calculadora-cubagem/096c2edb40c0e326b07cd7097fed6a8640a683ef/mbx_cargo.png"

# Criamos 3 colunas para centralizar a logo na tela
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(url_logo, use_container_width=True)

# 3. Título e Subtítulo
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Calculadora de Cubagem</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ferramenta oficial MBX Cargo para cálculo de peso taxável.</p>", unsafe_allow_html=True)
st.divider()

# 4. O formulário de cálculo
with st.form("form_cubagem"):
    st.markdown("**Dimensões dos volumes**")
    col_c, col_l, col_a = st.columns(3)
    with col_c:
        comprimento = st.number_input("Comprimento (cm)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    with col_l:
        largura = st.number_input("Largura (cm)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    with col_a:
        altura = st.number_input("Altura (cm)", min_value=0.0, value=0.0, step=1.0, format="%.2f")

    quantidade = st.number_input("Quantidade de volumes", min_value=1, value=1, step=1)

    st.markdown("**Informações de Peso e Frete**")
    col_f, col_p = st.columns(2)
    with col_f:
        # Deixei o valor padrão de 250kg/m3, muito usado no mercado, mas o usuário pode mudar
        fator = st.number_input("Fator de cubagem (kg/m³)", min_value=0.0, value=250.0, step=10.0, format="%.2f")
    with col_p:
        peso_real = st.number_input("Peso real total (kg)", min_value=0.0, value=0.0, step=1.0, format="%.2f")

    calcular = st.form_submit_button("Calcular Cubagem", use_container_width=True)

if calcular:
    if min(comprimento, largura, altura, fator, peso_real) <= 0:
        st.error("Todos os valores devem ser maiores que zero.")
    else:
        cubagem_unitaria = (comprimento * largura * altura) / 1000000
        cubagem_total = cubagem_unitaria * quantidade
        peso_cubado = cubagem_total * fator
        peso_taxavel = max(peso_real, peso_cubado)

        st.divider()
        st.subheader("Resultado do Cálculo")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Cubagem Total", f"{cubagem_total:.3f} m³")
            st.metric("Peso Cubado", f"{peso_cubado:.2f} kg")
        with c2:
            st.metric("Peso Real", f"{peso_real:.2f} kg")
            st.metric("Fator Utilizado", f"{fator:.0f} kg/m³")

        st.divider()
        
        # Destacando o Peso Taxável (Resultado final)
        st.markdown(f"<h3 style='text-align: center; color: #1E3A8A;'>PESO TAXÁVEL: {peso_taxavel:.2f} kg</h3>", unsafe_allow_html=True)
        
        if peso_real > peso_cubado:
            st.info("Critério utilizado: **Peso Real** (o peso real é maior que o cubado).")
        elif peso_cubado > peso_real:
            st.info("Critério utilizado: **Peso Cubado** (o volume ocupado compensa mais que o peso real).")
        else:
            st.info("Critério utilizado: **Pesos Iguais**.")
            
        st.caption("Cálculo realizado conforme padrões de logística e transporte.")

# 5. Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Desenvolvido para MBX Cargo. Todos os direitos reservados.</p>", unsafe_allow_html=True)