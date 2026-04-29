"""
Procesador Asientos ONVIO — placeholder
---------------------------------------
Cuando tengas listo el script de ONVIO, reemplazá esta página
siguiendo la misma estructura que procesador_iva.py:
  1. Funciones de lógica de negocio.
  2. UI con file_uploader + botón + download_button.
"""

import streamlit as st

st.title("📒 Procesador Asientos ONVIO")
st.info(
    "🛠️ Próximamente. Esta herramienta va a tomar el Excel molde con los "
    "asientos del papel de trabajo y devolverlo en el formato que pide ONVIO "
    "para importar."
)

st.markdown("### ¿Qué va a hacer?")
st.markdown(
    """
    - Recibir el **Excel molde** con los asientos como los armás vos.
    - Reordenar y mapear las columnas al formato ONVIO.
    - Devolver el Excel listo para importar.
    """
)
