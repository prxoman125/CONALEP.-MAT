import streamlit as st
import math

# Configuración de la página
st.set_page_config(
    page_title="Aproximación de Stirling",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Aproximación de Stirling y Análisis de Error")
st.markdown("Esta aplicación evalúa la **Serie de Stirling** para aproximar el factorial $x!$ (o $\Gamma(x+1)$) y la compara con el valor exacto.")

# Mostrar la fórmula matemática usando LaTeX
st.subheader("📌 Fórmula matemática")
st.latex(r"""
\Phi_A = \left(\frac{x}{e}\right)^x \cdot \sqrt{2\pi x} \cdot \left(1 + \frac{1}{12x} + \frac{1}{288x^2} - \frac{139}{51840x^3}\right)
""")

st.divider()

# Entrada del usuario para la variable x
st.subheader("⚙️ Configuración del valor $x$")
x = st.number_input(
    label="Ingresa o ajusta el valor de x (x > 0):",
    min_value=0.1,
    max_value=100.0,
    value=5.0,
    step=0.5,
    format="%.4f"
)

# Definición de funciones de cálculo
def calcular_aproximacion(x_val):
    termino_correccion = 1 + (1 / (12 * x_val)) + (1 / (288 * (x_val**2))) - (139 / (51840 * (x_val**3)))
    phi_a = ((x_val / math.e) ** x_val) * math.sqrt(2 * math.pi * x_val) * termino_correccion
    return phi_a

def calcular_exacto(x_val):
    return math.gamma(x_val + 1)

# Cálculos
valor_exacto = calcular_exacto(x)
valor_aprox = calcular_aproximacion(x)

error_absoluto = abs(valor_exacto - valor_aprox)
error_relativo_pct = (error_absoluto / valor_exacto) * 100
precision_pct = 100 - error_relativo_pct

st.divider()

# Resultados y métricas principales
st.subheader("📊 Resultados")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Valor Exacto (x!)", value=f"{valor_exacto:,.6f}")
with col2:
    st.metric(label="Valor Aproximado (Φ_A)", value=f"{valor_aprox:,.6f}")

st.subheader("🎯 Margen de Error y Precisión")

col3, col4, col5 = st.columns(3)
with col3:
    st.metric(label="Error Absoluto", value=f"{error_absoluto:.6e}")
with col4:
    st.metric(label="Error Relativo (%)", value=f"{error_relativo_pct:.6f}%")
with col5:
    st.metric(label="Precisión (%)", value=f"{precision_pct:.6f}%")

# Detalle desglosado de términos de la serie
with st.expander("🔍 Ver desglose de los términos de la fórmula"):
    t0 = (x / math.e)**x
    t1 = math.sqrt(2 * math.pi * x)
    c1 = 1 / (12 * x)
    c2 = 1 / (288 * (x**2))
    c3 = -139 / (51840 * (x**3))
    factor_correccion = 1 + c1 + c2 + c3

    st.write(f"- $(x/e)^x =$ `{t0:.8f}`")
    st.write(f"- $\\sqrt{{2\\pi x}} =$ `{t1:.8f}`")
    st.write(f"- Factor de corrección $(1 + \\frac{{1}}{{12x}} + \\frac{{1}}{{288x^2}} - \\frac{{139}}{{51840x^3}}) =$ `{factor_correccion:.10f}`")
 
