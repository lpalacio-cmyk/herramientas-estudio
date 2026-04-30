"""
Procesador Asientos ONVIO — versión web
---------------------------------------
Conversión del script transformador_onvio.py a Streamlit.
Mantiene la lógica original (melt + validación de partida doble) y agrega
dos formas de cargar datos:
  1. Grilla editable embebida (pegado directo desde Excel con Ctrl+V).
  2. Subir un archivo Excel (mismo formato que el .bat usaba).

Las columnas de meses en la grilla son de texto libre, así aceptan cualquier
formato de número que se pegue desde Excel: argentino (487.000,66), anglo
(487000.66), contable (paréntesis para negativos), con o sin símbolo de moneda.
"""

import io
from datetime import datetime, date
from calendar import monthrange

import pandas as pd
import streamlit as st


# ============================================================
#  Lógica de negocio
# ============================================================

NOMBRE_BASE_SALIDA = "Asientos_ONVIO"


def parsear_monto(valor) -> float:
    """
    Convierte cualquier formato de número a float.
    Acepta:
      - Argentino: 487.000,66 / -487.000,66
      - Anglo: 487000.66
      - US con miles: 487,000.66
      - Contable: (487.000,66) → negativo
      - Con moneda: $ 487.000,66
      - Vacío / None / NaN → 0.0
    """
    if pd.isna(valor) or valor is None:
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)

    s = str(valor).strip()
    if not s or s.lower() in ("nan", "none", "-"):
        return 0.0

    # Paréntesis = negativo (formato contable)
    negativo = False
    if s.startswith("(") and s.endswith(")"):
        negativo = True
        s = s[1:-1].strip()

    # Quitar símbolos de moneda y espacios (incl. no-break space)
    for c in ("$", "ARS", "USD", "€", " ", "\u00a0", "'"):
        s = s.replace(c, "")

    # Determinar separador decimal por posición del último signo
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            # AR: 487.000,66 → coma es decimal
            s = s.replace(".", "").replace(",", ".")
        else:
            # US: 487,000.66 → coma es miles
            s = s.replace(",", "")
    elif "," in s:
        # Solo coma → asumimos decimal (formato AR)
        s = s.replace(",", ".")
    # Solo punto → ya está en formato anglo, lo dejamos

    try:
        n = float(s)
        return -n if negativo else n
    except ValueError:
        return 0.0


def transformar(df_entrada: pd.DataFrame) -> tuple[pd.DataFrame | None, str]:
    """
    Toma el DataFrame con Código, Concepto y columnas de meses, y devuelve
    (df_resultado, mensaje). Si no balancea, devuelve (None, mensaje_de_error).
    """
    df = df_entrada.copy()

    if "Código" not in df.columns or "Concepto" not in df.columns:
        return None, "Faltan las columnas 'Código' y/o 'Concepto'."

    # Eliminar filas sin código (filas vacías que vienen de la grilla)
    df = df[df["Código"].notna() & (df["Código"].astype(str).str.strip() != "")].copy()

    if df.empty:
        return None, "No hay filas con datos para procesar."

    df["Orden_Original"] = df.index

    cols_fijas = ["Código", "Concepto", "Orden_Original"]
    cols_meses = [c for c in df.columns if c not in cols_fijas]

    if not cols_meses:
        return None, "No se encontraron columnas de meses para procesar."

    # Aplicar parser robusto a las columnas de meses (acepta cualquier formato)
    for col in cols_meses:
        df[col] = df[col].apply(parsear_monto)

    # Melt (desdinamizar)
    df_melted = df.melt(
        id_vars=cols_fijas,
        value_vars=cols_meses,
        var_name="Fecha_Cabecera",
        value_name="Monto",
    )

    df_melted = df_melted[df_melted["Monto"] != 0].copy()

    if df_melted.empty:
        return None, "Todas las celdas están en cero. No hay nada para importar."

    # Formato de fecha
    df_melted["Fecha_Cabecera"] = pd.to_datetime(
        df_melted["Fecha_Cabecera"], errors="coerce", dayfirst=True
    )

    if df_melted["Fecha_Cabecera"].isna().any():
        return None, "Hay encabezados de meses que no se pudieron interpretar como fecha."

    # Ordenar por fecha y orden original
    df_melted.sort_values(
        by=["Fecha_Cabecera", "Orden_Original"],
        ascending=[True, True],
        inplace=True,
    )

    # Numeración
    df_melted["Nro. Asiento"] = df_melted.groupby("Fecha_Cabecera").ngroup() + 1
    df_melted["Fecha Imputacion"] = df_melted["Fecha_Cabecera"].apply(
        lambda f: f + pd.offsets.MonthEnd(0)
    )
    df_melted["Nro. Pase"] = df_melted.groupby("Nro. Asiento").cumcount() + 1

    # Selección y renombre final
    df_final = df_melted[
        ["Nro. Asiento", "Nro. Pase", "Fecha Imputacion", "Código", "Concepto", "Monto"]
    ].copy()
    df_final.columns = [
        "Nro. Asiento",
        "Nro. Pase",
        "Fecha Imputacion",
        "Código de Cuenta",
        "Concepto/Descripción",
        "Monto",
    ]
    df_final["Fecha Imputacion"] = df_final["Fecha Imputacion"].dt.strftime("%d/%m/%Y")

    # Validación de partida doble (por asiento)
    sumas_por_asiento = df_final.groupby("Nro. Asiento")["Monto"].sum().round(2)
    desbalanceados = sumas_por_asiento[sumas_por_asiento != 0]

    if not desbalanceados.empty:
        detalle = ", ".join(
            f"Asiento #{n}: {v:,.2f}" for n, v in desbalanceados.items()
        )
        return None, (
            f"⚖️ Hay asientos que no balancean. Revisá los totales por mes en tu Excel.\n\n"
            f"Diferencias detectadas — {detalle}"
        )

    return df_final, "OK"


def df_a_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convierte el DataFrame final a un Excel en memoria."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Asientos")
    buffer.seek(0)
    return buffer.getvalue()


def fin_de_mes(anio: int, mes: int) -> date:
    """Devuelve el último día del mes."""
    return date(anio, mes, monthrange(anio, mes)[1])


def generar_columnas_meses(anio_inicio: int, mes_inicio: int, cantidad: int) -> list[str]:
    """Genera N columnas de fecha de fin de mes empezando desde un mes/año."""
    cols = []
    for i in range(cantidad):
        m = mes_inicio + i
        a = anio_inicio + (m - 1) // 12
        m = ((m - 1) % 12) + 1
        cols.append(fin_de_mes(a, m).strftime("%d/%m/%Y"))
    return cols


# ============================================================
#  Interfaz de usuario
# ============================================================

st.title("📒 Procesador Asientos ONVIO")
st.markdown(
    "Transformá el modelo de asiento del papel de trabajo (Código, Concepto, "
    "columnas por mes) al formato de filas que pide ONVIO para importar. "
    "Incluye validación automática de partida doble por asiento."
)

with st.expander("¿Cómo lo uso?"):
    st.markdown(
        """
        Tenés dos formas, elegí la que te resulte más cómoda:

        **🟢 Pegar en grilla** (más rápido para asientos chicos)
        1. Configurá el período fiscal (año y mes de inicio).
        2. Copiá las celdas de tu papel de trabajo en Excel — solo los datos,
           sin los encabezados.
        3. Hacé clic en la primera celda vacía de la grilla y pegá con `Ctrl+V`.
        4. Apretá **Procesar**.

        **🔵 Subir Excel** (igual que con el .bat de antes)
        1. Pegá los datos en tu Excel molde habitual y guardalo.
        2. Subilo en la pestaña correspondiente.
        3. Apretá **Procesar**.

        Si algún asiento no balancea (suma distinta de cero en un mes),
        la herramienta te avisa y **no genera el archivo**.

        💡 Los montos en la grilla aceptan cualquier formato: **argentino**
        (`487.000,66`), **anglo** (`487000.66`), o **contable** con paréntesis
        para negativos (`(487.000,66)`).
        """
    )

# --- Configuración del período ---
st.subheader("1. Configurar período")

col_a, col_b, col_c = st.columns([1, 1, 2])
anio_actual = datetime.now().year

with col_a:
    anio = st.number_input(
        "Año fiscal",
        min_value=2015,
        max_value=anio_actual + 1,
        value=anio_actual - 1,
        step=1,
        help="Año del que son los asientos.",
    )

with col_b:
    meses_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    mes_inicio_nombre = st.selectbox(
        "Primer mes",
        meses_es,
        index=0,
        help="Para años fiscales no calendario, elegí el mes de inicio.",
    )
    mes_inicio = meses_es.index(mes_inicio_nombre) + 1

with col_c:
    cantidad_meses = st.slider(
        "Cantidad de meses",
        min_value=1,
        max_value=12,
        value=12,
        help="Cuántos meses tiene el ejercicio. Casi siempre 12.",
    )

cols_meses = generar_columnas_meses(int(anio), mes_inicio, cantidad_meses)
st.caption(f"📅 Columnas que se van a generar: {' · '.join(cols_meses)}")

st.divider()

# --- Carga de datos ---
st.subheader("2. Cargar el asiento")

tab_grilla, tab_excel = st.tabs(["🟢 Pegar en grilla", "🔵 Subir Excel"])

df_resultado = None
mensaje = None

# ----- TAB 1: GRILLA EDITABLE -----
with tab_grilla:
    st.markdown(
        "Hacé clic en la primera celda vacía y pegá con `Ctrl+V` los datos "
        "copiados desde Excel. Podés agregar más filas con el `+` que aparece "
        "abajo a la derecha de la grilla."
    )
    st.caption(
        "✓ Acepta números en formato argentino (487.000,66), anglo (487000.66) "
        "o contable con paréntesis para negativos."
    )

    # DataFrame inicial vacío
    columnas = ["Código", "Concepto"] + cols_meses
    df_inicial = pd.DataFrame({col: [""] * 5 for col in columnas})

    # Configuración de columnas — TODAS de texto para aceptar cualquier formato
    column_config = {
        "Código": st.column_config.TextColumn(
            "Código",
            help="Código de cuenta contable (ej: 1.1.03.02.02)",
            width="medium",
        ),
        "Concepto": st.column_config.TextColumn(
            "Concepto",
            help="Descripción de la cuenta",
            width="large",
        ),
    }
    for col_mes in cols_meses:
        column_config[col_mes] = st.column_config.TextColumn(
            col_mes,
            help=f"Monto del mes {col_mes}. Acepta 487.000,66 o 487000.66",
            width="small",
        )

    df_editado = st.data_editor(
        df_inicial,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="grilla_onvio",
    )

    if st.button("Procesar (grilla)", type="primary", key="btn_grilla"):
        with st.spinner("Procesando..."):
            df_resultado, mensaje = transformar(df_editado)

# ----- TAB 2: SUBIR EXCEL -----
with tab_excel:
    st.markdown(
        "Subí el Excel del papel de trabajo (mismo formato que usabas con el "
        "`.bat`). Tiene que tener una hoja con las columnas Código, Concepto "
        "y una columna por mes."
    )

    archivo = st.file_uploader(
        "Excel del asiento",
        type=["xlsx", "xls"],
        key="archivo_onvio",
    )

    nombre_hoja = st.text_input(
        "Nombre de la hoja",
        value="Hoja1",
        help="Nombre de la pestaña dentro del Excel donde están los datos.",
    )

    if st.button("Procesar (Excel)", type="primary", disabled=not archivo, key="btn_excel"):
        try:
            df_subido = pd.read_excel(archivo, sheet_name=nombre_hoja)
            df_subido.columns = [
                c.strftime("%d/%m/%Y") if isinstance(c, (datetime, pd.Timestamp)) else c
                for c in df_subido.columns
            ]
            with st.spinner("Procesando..."):
                df_resultado, mensaje = transformar(df_subido)
        except Exception as e:
            mensaje = f"Error al leer el Excel: {e}"

# ============================================================
#  Resultado
# ============================================================

if mensaje is not None:
    st.divider()
    st.subheader("3. Resultado")

    if df_resultado is not None:
        st.success(f"✅ Asiento balanceado correctamente. {len(df_resultado)} líneas generadas.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Líneas totales", len(df_resultado))
        col2.metric("Asientos", df_resultado["Nro. Asiento"].nunique())
        col3.metric("Suma de montos", f"{df_resultado['Monto'].sum():,.2f}")

        with st.expander("Vista previa", expanded=True):
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{NOMBRE_BASE_SALIDA}_{timestamp}.xlsx"
        st.download_button(
            label=f"⬇️ Descargar {nombre_archivo}",
            data=df_a_excel_bytes(df_resultado),
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )
    else:
        st.error(mensaje)
