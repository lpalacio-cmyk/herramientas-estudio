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
