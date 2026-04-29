"""Página de inicio - landing del set de herramientas."""

import streamlit as st

st.title("Herramientas del Estudio")
st.markdown(
    "Set de utilidades internas para automatizar tareas repetitivas del flujo contable. "
    "Usá el menú de la izquierda para abrir la herramienta que necesites."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📑 Procesador Libro IVA")
    st.markdown(
        "Subís los ZIPs descargados de AFIP (uno o varios meses) y "
        "obtenés dos Excel consolidados — uno de **Ventas** y uno de **Compras** — "
        "listos para pegar en la base de control."
    )
    st.caption("Reemplaza el flujo de carpeta + .bat")

with col2:
    st.markdown("### 📒 Procesador Asientos ONVIO")
    st.markdown(
        "Subís el Excel molde con los asientos como los armás en los papeles "
        "de trabajo y lo recibís en el formato que pide ONVIO para importar."
    )
    st.caption("Próximamente")

st.divider()

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
