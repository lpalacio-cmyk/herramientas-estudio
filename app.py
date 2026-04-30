"""
Herramientas Estudio - App principal
"""

import streamlit as st

st.set_page_config(
    page_title="Herramientas Estudio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Fraunces', serif !important;
            letter-spacing: -0.02em;
        }
        .stButton > button {
            border-radius: 6px;
            font-weight: 500;
        }
        [data-testid="stFileUploader"] {
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

home = st.Page("paginas/home.py", title="Inicio", icon="🏠", default=True)
iva = st.Page("paginas/procesador_iva.py", title="Procesador Libro IVA", icon="📑")
onvio = st.Page("paginas/procesador_onvio.py", title="Procesador Asientos ONVIO", icon="📒")
f931 = st.Page("paginas/procesador_f931.py", title="Procesador F.931", icon="📄")
liq_carne = st.Page("paginas/liquidaciones_carne.py", title="Liquidaciones Compra Carne", icon="🥩")

pg = st.navigation(
    {
        "General": [home],
        "Herramientas": [iva, onvio, f931, liq_carne],
    }
)

pg.run()
