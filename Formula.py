import streamlit as st
import math
import time

st.set_page_config(
    page_title="Aproximacion de Stirling",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Forzar modo oscuro + ocultar Share y GitHub
st.markdown("""
    <style>
    /* Fondo degradado verde oscuro a negro */
   .stApp {
        background: linear-gradient(135deg, #021a0a 0%, #0a3d1a 40%, #000000 100%);
    }

    /* Ocultar barra superior completa (Share, GitHub, menu) */
    header[data-testid="stHeader"] {
        visibility: hidden!important;
        height: 0!important;
    }
    #MainMenu {visibility: hidden!important;}
    footer {visibility: hidden!important;}
    div[data-testid="stToolbar"] {display: none!important;}
    div[data-testid="stDecoration"] {display: none!important;}

    /* Forzar modo oscuro en todo el sistema */
    html, body, [data-testid="stAppViewContainer"] {
        color-scheme: dark!important;
    }

    /* Textos en blanco para que se vea en fondo oscuro */
    h1, h2, h3, p, label,.stMarkdown {
        color: white!important;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
    div[data-testid="stMetricLabel"] label, div[data-testid="stMetricValue"] div {
        color: white!important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Aproximacion de Stirling y Analisis de Error")
st.markdown("Esta aplicacion evalua la **Serie de Stirling** para aproximar el factorial $x!$ (o $\Gamma(x+1)$) y la compara con el valor exacto.")

st.subheader("Formula matematica")
st.latex(r"""
\Phi_A = \left(\frac{x}{e}\right)^x \cdot \sqrt{2\pi x} \cdot \left(1 + \frac{1}{12x} + \frac{1}{288x^2} - \frac{139}{51840x^3}\right)
""")

st.divider()

st.subheader("Configuracion del valor $x$")
x = st.number_input(
    label="Ingresa o ajusta el valor de x (x > 0):",
    min_value=0.1,
    max_value=120.0,
    value=5.0,
    step=0.1,
    format="%.4f"
)

def formato_dinamico(valor):
    return f"{valor:.6g}"

def calcular_aproximacion(x_val):
    termino_correccion = 1 + (1 / (12 * x_val)) + (1 / (288 * (x_val**2))) - (139 / (51840 * (x_val**3)))
    phi_a = ((x_val / math.e) ** x_val) * math.sqrt(2 * math.pi * x_val) * termino_correccion
    return phi_a

def calcular_exacto(x_val):
    return math.gamma(x_val + 1)

# Medicion de tiempo para cada calculo
t_inicio_exacto = time.perf_counter()
valor_exacto = calcular_exacto(x)
t_fin_exacto = time.perf_counter()
tiempo_exacto = t_fin_exacto - t_inicio_exacto

t_inicio_aprox = time.perf_counter()
valor_aprox = calcular_aproximacion(x)
t_fin_aprox = time.perf_counter()
tiempo_aprox = t_fin_aprox - t_inicio_aprox

error_absoluto = abs(valor_exacto - valor_aprox)
error_relativo_pct = (error_absoluto / valor_exacto) * 100
precision_pct = 100 - error_relativo_pct

st.divider()

st.subheader("Resultados")

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Valor Exacto (x!)", 
        value=formato_dinamico(valor_exacto),
        delta=f"Tiempo: {tiempo_exacto*1e6:.2f} µs",
        delta_color="off"
    )
with col2:
    st.metric(
        label="Valor Aproximado (Φ_A)", 
        value=formato_dinamico(valor_aprox),
        delta=f"Tiempo: {tiempo_aprox*1e6:.2f} µs",
        delta_color="off"
    )

st.subheader("Margen de Error y Precision")

col3, col4, col5 = st.columns(3)
with col3:
    st.metric(label="Error Absoluto", value=formato_dinamico(error_absoluto))
with col4:
    st.metric(label="Error Relativo (%)", value=f"{formato_dinamico(error_relativo_pct)}%")
with col5:
    st.metric(label="Precision (%)", value=f"{formato_dinamico(precision_pct)}%")

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
