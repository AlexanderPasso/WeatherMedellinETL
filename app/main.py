import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Clima Medellín", page_icon="🌤️", layout="wide")

@st.cache_data(ttl=600)
def get_data():
    df = pd.read_csv("data/master/clima_medellin.csv")
        
    # Crear columna datetime continua
    df['Fecha_Hora'] = pd.to_datetime(
        df['Fecha'].astype(str) + ' ' + df['Hora'].astype(str) + ':00:00'
    )
    
    df = df.sort_values(by='Fecha_Hora')
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
    val_max = df[columna_target].max()
    val_prom = df[columna_target].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Último Valor Registrado", f"{val_actual:.1f}")
    col2.metric("Valor Máximo Esperado", f"{val_max:.1f}")
    col3.metric("Promedio Esperado", f"{val_prom:.1f}")

st.divider()

# --- GRÁFICO PERSONALIZADO CON PLOTLY ---
st.subheader(f"Serie de Tiempo: {metrica_seleccionada}")

if 'Fecha_Hora' in df.columns and columna_target in df.columns:
    # 1. Crear figura de línea
    fig = px.line(
        df,
        x='Fecha_Hora',
        y=columna_target,
        labels={'Fecha_Hora': 'Fecha y Hora', columna_target: metrica_seleccionada},
        markers=True # Agrega puntos en cada registro horario para mejor visibilidad
    )

    # 2. Personalizar formato del eje X y fijar ALTO constante (400px)
    fig.update_layout(
        height=400, # Evita que el tamaño del gráfico cambie entre selecciones
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            tickformat="%d-%b %H:%M", # Formato legible: Ej. "28-Aug 12:00"
            dtick=43200000,           # Mostrar marca cada 12 horas (en milisegundos)
            showgrid=True
        ),
        yaxis=dict(showgrid=True)
    )

    # Estilar la línea
    fig.update_traces(line_color="#1f77b4", line_width=2.5)

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No se encontraron las columnas necesarias.")