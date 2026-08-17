import streamlit as st
import math
import time
import numpy as np
import plotly.graph_objects as go
import qrcode
from io import BytesIO
import base64

st.set_page_config(
    page_title="Aproximacion de Stirling",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Carga el logo
with open("Conalep-logo (1).png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #021a0a 0%, #0a3d1a 40%, #000000 100%);
        zoom: 0.8;
        min-height: 125vh;
    }}
    header[data-testid="stHeader"]{{visibility:hidden!important;height:0!important;}}
    #MainMenu{{visibility:hidden!important;}} 
    footer{{visibility:hidden!important;}}
    h1,h2,h3,p,label,.stMarkdown{{color:white!important;}}
    
    @keyframes flotarVertical {{
        0% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(8px);
        }}
        100% {{
            transform: translateY(0px);
        }}
    }}

    .logo-conalep-flotante {{
        zoom: 1.25;
        position: fixed;
        top: 20px;
        right: 15px;
        z-index: 9999999;
        width: 100px;
        background: rgba(255, 255, 255, 0.80);
        padding: 6px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        animation: flotarVertical 4s ease-in-out infinite;
    }}
    .logo-conalep-flotante img {{
        width: 100%;
        display: block;
    }}

    /* Media queries para adaptar perfectamente a dispositivos móviles */
    @media (max-width: 640px) {{
        .logo-conalep-flotante {{
            width: 65px;
            top: 10px;
            right: 10px;
        }}
        h1 {{
            font-size: 1.5rem !important;
            padding-right: 75px;
        }}
        .stNumberInput, .stMetric {{
            font-size: 0.9rem !important;
        }}
    }}
    </style>
    
    <div class="logo-conalep-flotante">
        <img src="data:image/png;base64,{logo_b64}">
    </div>
""", unsafe_allow_html=True)

st.markdown("#### CONALEP PLANTEL LEÓN 2")
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

st.divider()
st.subheader("Analisis Avanzado")

col_log1, col_log2 = st.columns(2)
with col_log1:
    st.metric("Log10(Valor Exacto)", f"{math.log10(valor_exacto):.6f}")
with col_log2:
    st.metric("Log10(Valor Aproximado)", f"{math.log10(valor_aprox):.6f}")

st.markdown("#### Convergencia del Error Relativo (0.5 a tu x actual)")
xs = np.linspace(0.5, x, 120)
errores = []
for v in xs:
    try:
        ex = calcular_exacto(v)
        ap = calcular_aproximacion(v)
        err = abs(ex - ap) / ex * 100
        errores.append(err)
    except:
        errores.append(0)

fig = go.Figure()
fig.add_trace(go.Scatter(x=xs, y=errores, mode='lines', line=dict(color='#00ff88', width=3), name='Error %'))
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Valor de x",
    yaxis_title="Error Relativo (%)",
    yaxis_type="log",
    height=270,
    margin=dict(l=20, r=20, t=10, b=10)
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Compartir App")

url_app = "https://conalep-mat-eshlocixhqvewkleadq5wc.streamlit.app/"

qr = qrcode.make(url_app)
buf = BytesIO()
qr.save(buf, format="PNG")

col_qr1, col_qr2 = st.columns([1, 2])
with col_qr1:
    st.image(buf, width=120)
with col_qr2:
    st.write("Escanea este QR para abrir la app en otro dispositivo:")
    st.code(url_app, language="text")
 
