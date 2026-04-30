"""
Herramientas Estudio - App principal
WL Hnos & Asoc - Identidad corporativa segun manual de marca
"""

import os
import streamlit as st

# --- Configuracion de la pagina ---------------------------------------------

LOGO_PATH = "assets/logo.png"
HAS_LOGO = os.path.exists(LOGO_PATH)

st.set_page_config(
    page_title="WL Hnos & Asoc · Herramientas",
    page_icon=LOGO_PATH if HAS_LOGO else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Logo en sidebar (Streamlit 1.31+)
if HAS_LOGO:
    try:
        st.logo(LOGO_PATH, size="large")
    except Exception:
        pass

# --- CSS de marca ------------------------------------------------------------

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Open+Sans:wght@400;500;600;700&display=swap');

        /* === Reset base === */
        html, body, [class*="css"], .stApp, .stMarkdown, p, span, div, label {
            font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* === Tipografia de titulos (Poppins per brand manual) === */
        h1, h2, h3, h4, h5, h6,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Poppins', sans-serif !important;
            color: #102250;
            letter-spacing: -0.015em;
            font-weight: 600;
        }

        h1 { font-weight: 700; font-size: 2.1rem; line-height: 1.2; }
        h2 { font-weight: 600; font-size: 1.6rem; }
        h3 { font-weight: 600; font-size: 1.25rem; }

        /* === Sidebar === */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FAFBFC 0%, #F0F3F8 100%);
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #102250;
        }

        /* Items del menu de navegacion */
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavLink"] {
            font-family: 'Open Sans', sans-serif;
            font-weight: 500;
            border-radius: 8px;
            transition: all 0.18s ease;
        }

        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNavLink"]:hover {
            background: rgba(21, 149, 188, 0.08);
        }

        /* Logo en sidebar - margen */
        [data-testid="stLogo"] {
            margin: 0.5rem 0 1rem 0;
        }

        /* === Botones === */
        .stButton > button,
        .stDownloadButton > button {
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            border-radius: 8px;
            border: 1.5px solid transparent;
            transition: all 0.18s ease;
            padding: 0.5rem 1.1rem;
        }

        .stButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"] {
            background: #102250;
            color: #FFFFFF;
            border-color: #102250;
        }

        .stButton > button[kind="primary"]:hover,
        .stDownloadButton > button[kind="primary"]:hover {
            background: #1595BC;
            border-color: #1595BC;
            box-shadow: 0 6px 16px rgba(21, 149, 188, 0.25);
            transform: translateY(-1px);
        }

        .stButton > button[kind="secondary"] {
            background: #FFFFFF;
            color: #102250;
            border-color: #E2E8F0;
        }

        .stButton > button[kind="secondary"]:hover {
            border-color: #1595BC;
            color: #1595BC;
            background: #F0F9FC;
        }

        /* === File uploader === */
        [data-testid="stFileUploader"] section {
            border: 2px dashed #CBD5E1;
            background: #FAFBFC;
            border-radius: 12px;
            padding: 1.25rem;
            transition: all 0.18s ease;
        }

        [data-testid="stFileUploader"] section:hover {
            border-color: #1595BC;
            background: #F0F9FC;
        }

        [data-testid="stFileUploader"] button {
            background: #102250 !important;
            color: white !important;
            border-radius: 6px !important;
            font-family: 'Poppins', sans-serif !important;
        }

        /* === Data editor / dataframe === */
        [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #E5E7EB;
        }

        /* === Alertas (info / success / warning / error) === */
        [data-testid="stAlert"] {
            border-radius: 10px;
            border-left-width: 4px;
            font-family: 'Open Sans', sans-serif;
        }

        /* === Progress bar === */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #1595BC, #102250);
        }

        /* === Inputs === */
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stSelectbox > div > div {
            border-radius: 7px;
            border-color: #E2E8F0;
            font-family: 'Open Sans', sans-serif;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {
            border-color: #1595BC;
            box-shadow: 0 0 0 2px rgba(21, 149, 188, 0.15);
        }

        /* === Tabs === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            border-bottom: 1px solid #E5E7EB;
        }

        .stTabs [data-baseweb="tab"] {
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            color: #6C6D6D;
        }

        .stTabs [aria-selected="true"] {
            color: #102250 !important;
        }

        /* === Expander === */
        [data-testid="stExpander"] {
            border-radius: 10px;
            border: 1px solid #E5E7EB;
            background: #FAFBFC;
        }

        [data-testid="stExpander"] summary {
            font-family: 'Open Sans', sans-serif;
            font-weight: 500;
            color: #102250;
        }

        /* === Code === */
        code {
            background: #F1F5F9;
            color: #102250;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 0.88em;
            font-family: 'Menlo', 'Monaco', monospace;
        }

        /* === Captions === */
        [data-testid="stCaptionContainer"], small {
            color: #6C6D6D;
            font-size: 0.875rem;
            font-family: 'Open Sans', sans-serif;
        }

        /* === Divider === */
        hr {
            border-color: #E5E7EB;
            margin: 1.75rem 0;
        }

        /* === Eliminamos el header default === */
        [data-testid="stHeader"] {
            background: transparent;
        }

        /* ============================================================
           Componentes de la pagina HOME (cards, hero, etc)
           ============================================================ */

        .hero {
            padding: 1.5rem 0 2.25rem 0;
            margin-bottom: 1rem;
            border-bottom: 1px solid #F1F5F9;
        }

        .hero-eyebrow {
            display: inline-block;
            color: #1595BC;
            font-family: 'Poppins', sans-serif;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.85rem;
            padding: 4px 12px;
            background: rgba(21, 149, 188, 0.08);
            border-radius: 20px;
        }

        .hero h1 {
            font-family: 'Poppins', sans-serif !important;
            font-size: 2.6rem;
            font-weight: 700;
            color: #102250;
            margin: 0 0 0.85rem 0;
            line-height: 1.1;
            letter-spacing: -0.025em;
        }

        .hero p.subtitle {
            font-family: 'Open Sans', sans-serif;
            color: #6C6D6D;
            font-size: 1.1rem;
            max-width: 720px;
            line-height: 1.6;
            margin: 0;
        }

        /* Grid de tarjetas */
        .tool-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.25rem;
            margin: 1.5rem 0;
        }

        .tool-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1.6rem;
            transition: all 0.22s ease;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }

        .tool-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #102250 0%, #1595BC 100%);
            opacity: 0;
            transition: opacity 0.22s ease;
        }

        .tool-card:hover {
            border-color: #1595BC;
            transform: translateY(-3px);
            box-shadow: 0 14px 32px rgba(16, 34, 80, 0.08);
        }

        .tool-card:hover::before {
            opacity: 1;
        }

        .tool-card-icon {
            width: 52px;
            height: 52px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1.1rem;
            background: linear-gradient(135deg, #102250 0%, #1595BC 100%);
            box-shadow: 0 6px 16px rgba(16, 34, 80, 0.18);
        }

        .tool-card h3 {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            font-size: 1.1rem;
            color: #102250;
            margin: 0 0 0.65rem 0;
            line-height: 1.3;
        }

        .tool-card p {
            font-family: 'Open Sans', sans-serif;
            color: #4B5563;
            font-size: 0.93rem;
            line-height: 1.55;
            flex-grow: 1;
            margin: 0 0 1rem 0;
        }

        .tool-card-tag {
            display: inline-block;
            background: #F0F9FC;
            color: #1595BC;
            font-family: 'Open Sans', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 4px 11px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            align-self: flex-start;
        }

        /* Footer info */
        .home-footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #F1F5F9;
            color: #6C6D6D;
            font-size: 0.85rem;
            font-family: 'Open Sans', sans-serif;
        }

        .home-footer strong {
            color: #102250;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Navegacion -------------------------------------------------------------

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
