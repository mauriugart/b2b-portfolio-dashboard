import streamlit as st
import pandas as pd

st.set_page_config(page_title="Automated B2B Dashboard", layout="wide")
st.title("📈 B2B Client Portfolio Automation")

uploaded_file = st.file_uploader("Upload your raw monthly report (CSV) here:", type=["csv"])

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    
    # 1. Motor de limpieza (ETL)
    diccionario_limpieza = {r'[\$,]': '', r' USD': '', r' ': ''}
    df['Annual_Revenue'] = df['Annual_Revenue'].replace(diccionario_limpieza, regex=True)
    df['Annual_Revenue'] = pd.to_numeric(df['Annual_Revenue'], errors='coerce')
    
    df['Status'] = df['Status'].str.strip().str.upper()
    df['Renewal_Date'] = pd.to_datetime(df['Renewal_Date'], errors='coerce')
    df['Company_Name'] = df['Company_Name'].str.strip()
    df['Industry'] = df['Industry'].str.strip()
    
    st.success("Data processed and cleaned in milliseconds!")

    # 2. Interfaz del usuario: Menú desplegable dinámico
    st.subheader("Filter Portfolio by Status")
    
    # Obtenemos los valores únicos de la columna Status (ej. ['ACTIVE', 'INACTIVE'])
    opciones_estado = df['Status'].dropna().unique()
    estado_seleccionado = st.selectbox("Select Client Status:", opciones_estado)

    # 3. Filtrado y cálculos basados en la elección del usuario
    df_filtrado = df[df['Status'] == estado_seleccionado]
    ingreso_filtrado = df_filtrado['Annual_Revenue'].sum()
    
    # El título de la métrica cambia automáticamente (ej. "ACTIVE Clients Revenue")
    st.metric(f"{estado_seleccionado} Clients Revenue", f"${ingreso_filtrado:,.2f}")
    
    st.subheader(f"Normalized Database ({estado_seleccionado})")
    st.dataframe(df_filtrado)
    
else:
    st.info("Waiting for data... Drag and drop your current month's CSV file to begin.")