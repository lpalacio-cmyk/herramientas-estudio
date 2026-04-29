# Herramientas Estudio

Set de herramientas internas del estudio, accesibles vía web. Construido con
Streamlit. Cada herramienta es una página independiente dentro de la misma app.

## Estructura

```
herramientas-estudio/
├── app.py                       # Punto de entrada y navegación
├── requirements.txt             # Dependencias
├── .streamlit/
│   └── config.toml              # Tema visual y configuración
└── paginas/
    ├── home.py                  # Landing
    ├── procesador_iva.py        # Procesador Libro IVA (listo)
    └── procesador_onvio.py      # Procesador ONVIO (placeholder)
```

## Probarlo en tu compu (antes de subirlo)

```bash
# 1. Crear un entorno virtual (opcional pero recomendado)
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # Mac / Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr la app
streamlit run app.py
```

Se abre solo en `http://localhost:8501`.

## Deployar en Streamlit Community Cloud (gratis)

1. Subí esta carpeta a un repo de GitHub (puede ser privado).
2. Entrá a https://share.streamlit.io e iniciá sesión con GitHub.
3. **New app** → seleccionás el repo, la rama y el archivo `app.py`.
4. Deploy. En 2-3 minutos tenés una URL tipo `tuestudio.streamlit.app`.

### Restringir el acceso al equipo

En los **Settings** de la app, sección **Sharing**, activá *"This app is private"*
y agregá los emails de tus compañeros. Solo ellos van a poder entrar después de
loguearse con Google.

## Agregar una herramienta nueva

1. Crear un archivo en `paginas/` (por ejemplo `paginas/procesador_pdf.py`).
2. Escribir la lógica de la herramienta usando widgets de Streamlit:
   - `st.file_uploader(...)` para recibir archivos.
   - `st.download_button(...)` para devolver resultados.
3. Registrarla en `app.py`:
   ```python
   pdf = st.Page("paginas/procesador_pdf.py", title="Procesador PDF", icon="📄")
   pg = st.navigation({
       "General": [home],
       "Herramientas": [iva, onvio, pdf],   # ← agregar acá
   })
   ```

Listo. Aparece sola en el menú lateral.

## Notas

- Los archivos subidos viven solo en memoria mientras dura el procesamiento.
  No se guardan en el servidor.
- El límite de subida está en 500 MB por archivo (ajustable en
  `.streamlit/config.toml`).
