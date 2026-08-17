import streamlit as st
import math

# Configuración de la página
st.set_page_config(
    page_title="Aproximacion de Stirling",
    page_icon="",
    layout="centered"
)

# CSS para fondo degradado verde oscuro con negro y quitar emojis visuales
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #021a0a 0%, #0a3d1a 40%, #000000 100%);
    }
    h1, h2, h3, p, label, .stMetricLabel, .stMetricValue {
        color: white !important;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
    .stExpander {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Aproximacion de Stirling y Analisis de Error")
st.markdown("Esta aplicacion evalua la **Serie de Stirling** para aproximar el factorial $x!$ (o $\Gamma(x+1)$) y la compara con el valor exacto.")

# Mostrar la fórmula matemática usando LaTeX
st.subheader("Formula matematica")
st.latex(r"""
\Phi_A = \left(\frac{x}{e}\right)^x \cdot \sqrt{2\pi x} \cdot \left(1 + \frac{1}{12x} + \frac{1}{288x^2} - \frac{139}{51840x^3}\right)
""")

st.divider()

# Entrada del usuario para la variable x
st.subheader("Configuracion del valor $x$")
x = st.number_input(
    label="Ingresa o ajusta el valor de x (x > 0):",
    min_value=0.1,
    max_value=100.0,
    value=5.0,
    step=0.5,
    format="%.4f"
)

# Funcion para formato dinamico - solo decimales necesarios
def formato_dinamico(valor):
    # Usa formato 'g' que quita ceros innecesarios y ajusta automaticamente
    return f"{valor:.6g}"

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
st.subheader("Resultados")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Valor Exacto (x!)", value=formato_dinamico(valor_exacto))
with col2:
    st.metric(label="Valor Aproximado (Φ_A)", value=formato_dinamico(valor_aprox))

st.subheader("Margen de Error y Precision")

col3, col4, col5 = st.columns(3)
with col3:
    st.metric(label="Error Absoluto", value=formato_dinamico(error_absoluto))
with col4:
    st.metric(label="Error Relativo (%)", value=f"{formato_dinamico(error_relativo_pct)}%")
with col5:
    st.metric(label="Precision (%)", value=f"{formato_dinamico(precision_pct)}%")

# Detalle desglosado de términos de la serie
with st.expander("Ver desglose de los terminos de la formula"):
    t0 = (x / math.e)**x
    t1 = math.sqrt(2 * math.pi * x)
    c1 = 1 / (12 * x)
    c2 = 1 / (288 * (x**2))
    c3 = -139 / (51840 * (x**3))
    factor_correccion = 1 + c1 + c2 + c3

    st.write(f"- $(x/e)^x =$ `{formato_dinamico(t0)}`")
    st.write(f"- $\\sqrt{{2\\pi x}} =$ `{formato_dinamico(t1)}`")
    st.write(f"- $1/(12x) =$ `{formato_dinamico(c1)}`")
    st.write(f"- $1/(288x^2) =$ `{formato_dinamico(c2)}`")
    st.write(f"- $-139/(51840x^3) =$ `{formato_dinamico(c3)}`")
    st.write(f"- Factor de correccion total =$ `{formato_dinamico(factor_correccion)}`")
