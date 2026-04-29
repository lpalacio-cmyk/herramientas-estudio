"""
Herramientas Estudio - App principal
------------------------------------
Punto de entrada de la app. Define la navegación entre las distintas
herramientas. Para agregar una nueva, creá un archivo en paginas/
y sumalo en la lista pages de abajo.
"""

import streamlit as st

st.set_page_config(
    page_title="Herramientas Estudio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos globales (tipografía y colores sobrios para contexto contable)
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
        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 500;
            background: #1F4E79;
            color: white;
            margin-left: 8px;
        }
        .badge-soon {
            background: #6c757d;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Definición de páginas
home = st.Page("paginas/home.py", title="Inicio", icon="🏠", default=True)
iva = st.Page("paginas/procesador_iva.py", title="Procesador Libro IVA", icon="📑")
onvio = st.Page("paginas/procesador_onvio.py", title="Procesador Asientos ONVIO", icon="📒")

pg = st.navigation(
    {
        "General": [home],
        "Herramientas": [iva, onvio],
    }
)

pg.run()
