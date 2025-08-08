import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv(
  "leei.csv",
  header=None,
  names=['#', 'RELATÓRIO', 'NOME', 'MUNICÍPIO', 'UF', 'TURMA', 'CONTRATO', 'OFÍCIO', 'DATA'],
)

st.dataframe(
  df,
  hide_index=True
)

# Gráfico com o Streamlit
st.bar_chart(df['UF'].value_counts())

# Gráfico com o Altair
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

st.altair_chart(chart, use_container_width=True)
