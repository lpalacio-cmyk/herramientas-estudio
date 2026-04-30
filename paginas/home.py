"""Pagina de inicio - landing del set de herramientas."""

import streamlit as st

# --- Hero ---
st.html("""
<div class="hero">
<span class="hero-eyebrow">WL Hnos &amp; Asoc · Estudio Contable</span>
<h1>Herramientas del Estudio</h1>
<p class="subtitle">Set de utilidades internas para automatizar tareas repetitivas del flujo contable. Elegí una herramienta en el menú lateral para empezar.</p>
</div>
""")

# --- Tarjetas ---
st.html("""
<div class="tool-grid">

<div class="tool-card">
<div class="tool-card-icon">📑</div>
<h3>Procesador Libro IVA</h3>
<p>Subís los ZIPs descargados de AFIP (uno o varios meses) y obtenés dos Excel consolidados — Ventas y Compras — listos para pegar en la base de control.</p>
<span class="tool-card-tag">Reemplaza el .bat</span>
</div>

<div class="tool-card">
<div class="tool-card-icon">📒</div>
<h3>Procesador Asientos ONVIO</h3>
<p>Pegás el asiento desde Excel directo en una grilla web (o subís el archivo) y obtenés el Excel listo para importar a ONVIO. Valida partida doble por asiento.</p>
<span class="tool-card-tag">Reemplaza el .bat</span>
</div>

<div class="tool-card">
<div class="tool-card-icon">📄</div>
<h3>Procesador F.931</h3>
<p>Subís los PDFs del formulario 931 de ARCA (hasta 12 a la vez) y extrae los datos clave por OCR. Grilla editable y Excel resumen para copiar al papel de trabajo.</p>
<span class="tool-card-tag">Automatiza F.931</span>
</div>

<div class="tool-card">
<div class="tool-card-icon">🥩</div>
<h3>Liquidaciones Compra Carne</h3>
<p>Subís los PDFs de liquidaciones (LCD, LCDP, LC) de ARCA y obtenés un Excel consolidado con TIPO, CPTE, FECHA, KG y $ BRUTO. Detecta ajustes físicos de crédito y suma comisiones de LC.</p>
<span class="tool-card-tag">Reemplaza carga manual</span>
</div>

</div>
""")

# --- Info expandible ---
with st.expander("ℹ️ Sobre estas herramientas"):
    st.markdown(
        """
        - **No se guardan archivos en el servidor.** Cada procesamiento es en memoria
          y los archivos se descartan al cerrar la sesión.
        - Si una herramienta tira error, copiá el mensaje y avisá para que se ajuste.
        - Para sumar una nueva herramienta, se agrega un archivo en `paginas/` y
          aparece sola en el menú.
        """
    )

# --- Footer ---
st.html(
    '<div class="home-footer"><strong>WL Hnos &amp; Asoc</strong> · '
    'Estudio Contable · Catamarca, Argentina</div>'
)
