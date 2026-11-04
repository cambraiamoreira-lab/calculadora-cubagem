import streamlit as st

st.set_page_config(
    page_title="CargoCalc - Calculadora de Cubagem",
    page_icon="📦"
)

st.title("📦 CargoCalc")
st.subheader("Calculadora de Cubagem")
st.caption("Informe as dimensões dos volumes para calcular o peso taxável.")

with st.form("form_cubagem"):
    st.markdown("**Dimensões dos volumes**")
    col1, col2, col3 = st.columns(3)
    with col1:
        comprimento = st.number_input("Comprimento (cm)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    with col2:
        largura = st.number_input("Largura (cm)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    with col3:
        altura = st.number_input("Altura (cm)", min_value=0.0, value=0.0, step=1.0, format="%.2f")

    quantidade = st.number_input("Quantidade de volumes", min_value=1, value=1, step=1)

    col4, col5 = st.columns(2)
    with col4:
        fator = st.number_input("Fator de cubagem (kg/m³)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    with col5:
        peso_real = st.number_input("Peso real total (kg)", min_value=0.0, value=0.0, step=1.0, format="%.2f")

    calcular = st.form_submit_button("Calcular", use_container_width=True)

if calcular:
    if min(comprimento, largura, altura, fator, peso_real) <= 0:
        st.error("Todos os valores devem ser positivos.")
    else:
        cubagem_unitaria = (comprimento * largura * altura) / 1000000
        cubagem_total = cubagem_unitaria * quantidade
        peso_cubado = cubagem_total * fator
        peso_taxavel = max(peso_real, peso_cubado)

        st.divider()
        st.subheader("Resultado")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Cubagem por volume", f"{cubagem_unitaria:.3f} m³")
            st.metric("Cubagem total", f"{cubagem_total:.3f} m³")
            st.metric("Fator utilizado", f"{fator:.2f} kg/m³")
        with c2:
            st.metric("Quantidade de volumes", quantidade)
            st.metric("Peso real", f"{peso_real:.2f} kg")
            st.metric("Peso cubado", f"{peso_cubado:.2f} kg")

        st.divider()
        st.metric("⚖️ PESO TAXÁVEL", f"{peso_taxavel:.2f} kg")

        if peso_real > peso_cubado:
            st.info("Critério: **Peso real**")
        elif peso_cubado > peso_real:
            st.info("Critério: **Peso cubado**")
        else:
            st.info("Critério: **Pesos iguais**")

        st.success("Cálculo concluído!")