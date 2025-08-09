import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv(
  "leei.csv",
  header=None,
  names=['#', 'RELATÓRIO', 'NOME', 'MUNICÍPIO', 'UF', 'TURMA', 'CONTRATO', 'OFÍCIO', 'DATA'],
)

# Gráfico 1: barras horizontais com Altair
frequency_series = df['UF'].value_counts()

frequency_df = frequency_series.reset_index()
frequency_df.columns = ['Category', 'Count']

chart = alt.Chart(frequency_df).mark_bar().encode(
    y=alt.Y('Category:N', title='Category'),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title='Frequency'),    # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title='Número de solicitações de pagamento por UF'
)

# Gráfico 2: barras verticais com Streamlit e filtro
relatorios  = df["RELATÓRIO"].value_counts().index
relatorio = st.sidebar.selectbox("RELATÓRIO", relatorios)
df_filtered = df[df["RELATÓRIO"] == relatorio]

# Layout com colunas
col1, col2 = st.columns(2, gap="large")

with col1:
  st.header("Raw data")
  st.dataframe(
    df,
    hide_index=True
  )

with col2:
  st.header("Graphics")
  st.altair_chart(chart, use_container_width=True) # Gráfico 1
  st.bar_chart(df_filtered['UF'].value_counts())   # Gráfico 2
