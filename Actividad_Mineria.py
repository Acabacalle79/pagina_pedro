# -*- coding: utf-8 -*-
# Dashboard de Análisis de Datos Universitarios con Streamlit

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Título del dashboard
st.title("University Data Analysis Dashboard")
st.write("Análisis visual de tasas de retención y satisfacción estudiantil.")

# Cargar archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV (university_student_data.csv)", type=["csv"])

if uploaded_file is not None:
    # Leer datos
    df = pd.read_csv(uploaded_file)
    
    # Mostrar información básica
    st.subheader("Vista general de los datos")
    st.dataframe(df.head())

    # Limpiar y preparar datos
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Retention Rate (%)"] = df["Retention Rate (%)"].astype(str).str.replace('%','', regex=False).astype(float)
    df["Student Satisfaction (%)"] = df["Student Satisfaction (%)"].astype(str).str.replace('%','', regex=False).astype(float)

    # Gráfica 1: Retention rate trends
    st.subheader("📈 Retention Rate Trends Over Time")
    fig1, ax1 = plt.subplots(figsize=(8,5))
    sns.lineplot(data=df, x="Year", y="Retention Rate (%)", marker="o", ax=ax1)
    ax1.set_title("Retention Rate Trends Over Time")
    ax1.set_ylabel("Retention Rate (%)")
    st.pyplot(fig1)

    # Gráfica 2: Student satisfaction scores
    st.subheader("📊 Student Satisfaction by Year")
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(data=df, x="Year", y="Student Satisfaction (%)", palette="coolwarm", ax=ax2)
    ax2.set_title("Student Satisfaction by Year")
    ax2.set_ylabel("Average Satisfaction (%)")
    st.pyplot(fig2)

    # Gráfica 3: Comparison between Spring and Fall
    st.subheader("Retention Rate by Term")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.boxplot(data=df, x="Term", y="Retention Rate (%)", palette="Set2", ax=ax3)
    ax3.set_title("Retention Rate Comparison: Spring vs Fall")
    ax3.set_ylabel("Retention Rate (%)")
    st.pyplot(fig3)

    # Agrupar datos
    retention_year = df.groupby("Year")["Retention Rate (%)"].mean().reset_index()
    satisfaction_year = df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()
    term_comparison = df.groupby("Term")["Retention Rate (%)"].mean().reset_index()

    # Mostrar tablas resumidas
    st.subheader("Promedios por Año y por Término")
    st.write("**Retention Rate por Año:**")
    st.dataframe(retention_year)
    st.write("**Satisfaction por Año:**")
    st.dataframe(satisfaction_year)
    st.write("**Retention Rate por Término:**")
    st.dataframe(term_comparison)

else:
    st.warning("Por favor sube un archivo CSV para comenzar.")
