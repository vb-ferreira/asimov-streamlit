import streamlit as st
import pandas as pd
import altair as alt

# Data
df = st.session_state['df_leei']

# Solicitações por UF
frequency_series_uf = df['UF'].value_counts()

frequency_uf = frequency_series_uf.reset_index()
frequency_uf.columns = ['Category', 'Count']

chart_1 = alt.Chart(frequency_uf).mark_bar().encode(
    y=alt.Y('Category:N', title=''),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title=''),     # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title='Número de solicitações de pagamento por UF'
)

# Solicitações por Relatório
frequency_series_rel = df['RELATÓRIO'].value_counts()

frequency_rel = frequency_series_rel.reset_index()
frequency_rel.columns = ['Category', 'Count']

custom_order = ["RELATÓRIO 1", "RELATÓRIO 2", "RELATÓRIO 3", "RELATÓRIO 4", "RELATÓRIO 5",
                "RELATÓRIO 6", "RELATÓRIO 7", "RELATÓRIO 8", "RELATÓRIO 9", "RELATÓRIO 10"]

chart_2 = alt.Chart(frequency_rel).mark_bar().encode(
    y=alt.Y('Category:N', sort=custom_order, title=''),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title=''),     # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title='Número de solicitações de pagamento por relatório'
)

# Plot
st.altair_chart(chart_1, use_container_width=True)
st.altair_chart(chart_2, use_container_width=True)
