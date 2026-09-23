import io

import boto3
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

cutoff_date_act = datetime.now(
        ZoneInfo("America/Bogota")
    ).strftime("%Y-%m-%d")

st.set_page_config(
    page_title="Clima Medellín",
    page_icon="🌤️",
    layout="wide"
)


BUCKET = "etl-clima-medellin-data"
KEY = "master/clima_medellin.csv"

s3 = boto3.client("s3")


@st.cache_data(ttl=600)
def get_data():

    response = s3.get_object(
        Bucket=BUCKET,
        Key=KEY
    )

    df = pd.read_csv(
        io.BytesIO(response["Body"].read())
    )

    # Crear columna datetime continua
    df["Fecha_Hora"] = pd.to_datetime(
        df["Fecha"].astype(str)
        + " "
        + df["Hora"].astype(str)
        + ":00:00"
    )

    df = df.sort_values(by="Fecha_Hora")

    return df


df = get_data()

st.title("🌤️ Dashboard Predicción del Clima en Medellín")

# --- BARRA LATERAL ---
st.sidebar.header("Opciones de Configuración")

opciones_metricas = {
    "Temperatura (°C)": "Temperatura",
    "Lluvia (mm)": "Lluvia",
    "Probabilidad de Lluvia (%)": "Probabilidad_Lluvia"
}

metrica_seleccionada = st.sidebar.selectbox(
    "Selecciona la variable a visualizar:",
    options=list(opciones_metricas.keys())
)

columna_target = opciones_metricas[metrica_seleccionada]

# --- MÉTRICAS DE RESUMEN ---
if not df.empty and columna_target in df.columns:

    val_actual = df[columna_target].iloc[-1]
    val_max = df.loc[df["Fecha"] == cutoff_date_act,columna_target].max()
    val_prom = df.loc[df["Fecha"] == cutoff_date_act,columna_target].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Último Valor Registrado",
        f"{val_actual:.1f}"
    )

    col2.metric(
        "Valor Máximo Esperado",
        f"{val_max:.1f}"
    )

    col3.metric(
        "Promedio Esperado",
        f"{val_prom:.1f}"
    )

st.divider()

# --- GRÁFICO ---
st.subheader(
    f"Serie de Tiempo: {metrica_seleccionada}"
)

if "Fecha_Hora" in df.columns and columna_target in df.columns:

    fig = px.line(
        df,
        x="Fecha_Hora",
        y=columna_target,
        labels={
            "Fecha_Hora": "Fecha y Hora",
            columna_target: metrica_seleccionada
        },
        markers=True
    )

    fig.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        xaxis=dict(
            tickformat="%d-%b %H:%M",
            dtick=43200000,
            showgrid=True
        ),
        yaxis=dict(
            showgrid=True
        )
    )

    fig.update_traces(
        line_color="#1f77b4",
        line_width=2.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.error(
        "No se encontraron las columnas necesarias."
    )