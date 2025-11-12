
# -*- coding: utf-8 -*-
# Streamlit Dashboard - University Data Analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ------------------------------------
# CONFIGURACIÓN DE LA APP
# ------------------------------------
st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("🎓 University Student Data Dashboard")
st.write("Análisis interactivo de tasas de retención, satisfacción y comparación entre términos académicos.")

# ------------------------------------
# CARGA DEL DATASET
# ------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("university_student_data.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Retention Rate (%)"] = df["Retention Rate (%)"].astype(str).str.replace('%','', regex=False).astype(float)
    df["Student Satisfaction (%)"] = df["Student Satisfaction (%)"].astype(str).str.replace('%','', regex=False).astype(float)
    return df

df = load_data()

# ------------------------------------
# FILTROS INTERACTIVOS
# ------------------------------------
st.sidebar.header("Filtros")
years = sorted(df["Year"].dropna().unique())
terms = df["Term"].dropna().unique()
departments = df["Department"].dropna().unique() if "Department" in df.columns else []

selected_year = st.sidebar.multiselect("Seleccionar año(s):", years, default=years)
selected_term = st.sidebar.multiselect("Seleccionar término(s):", terms, default=terms)
if len(departments) > 0:
    selected_dept = st.sidebar.multiselect("Seleccionar departamento(s):", departments, default=departments)
else:
    selected_dept = []

# Filtrado de datos
filtered_df = df[
    df["Year"].isin(selected_year) &
    df["Term"].isin(selected_term)
]
if len(selected_dept) > 0:
    filtered_df = filtered_df[filtered_df["Department"].isin(selected_dept)]

# ------------------------------------
# VISUALIZACIONES
# ------------------------------------
st.subheader("📈 Retention Rate Trends Over Time")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.lineplot(data=filtered_df, x="Year", y="Retention Rate (%)", marker="o", ax=ax1)
ax1.set_title("Retention Rate Trends Over Time")
ax1.set_ylabel("Retention Rate (%)")
st.pyplot(fig1)

st.subheader("🎯 Student Satisfaction by Year")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=filtered_df, x="Year", y="Student Satisfaction (%)", palette="coolwarm", ax=ax2)
ax2.set_title("Student Satisfaction by Year")
ax2.set_ylabel("Average Satisfaction (%)")
st.pyplot(fig2)

st.subheader("📊 Comparison Between Spring and Fall Terms")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.boxplot(data=filtered_df, x="Term", y="Retention Rate (%)", palette="Set2", ax=ax3)
ax3.set_title("Retention Rate: Spring vs Fall")
st.pyplot(fig3)

# ------------------------------------
# KPIs o indicadores
# ------------------------------------
st.subheader("🔍 Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Average Retention Rate", f"{filtered_df['Retention Rate (%)'].mean():.2f}%")
col2.metric("Average Student Satisfaction", f"{filtered_df['Student Satisfaction (%)'].mean():.2f}%")
col3.metric("Total Records", len(filtered_df))

# ------------------------------------
# NOTA FINAL
# ------------------------------------
st.info("💡 Tip: Usa los filtros de la barra lateral para explorar distintos años, términos o departamentos.")

