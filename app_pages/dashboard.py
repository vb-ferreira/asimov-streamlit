import streamlit as st
import pandas as pd
import altair as alt

df = st.session_state['df_leei']

frequency_series = df['UF'].value_counts()

frequency_df = frequency_series.reset_index()
frequency_df.columns = ['Category', 'Count']

chart = alt.Chart(frequency_df).mark_bar().encode(
    y=alt.Y('Category:N', title=''),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title='Nº de solicitações'),    # 'Q' para dados quantitativos
    # tooltip=['Category', 'Count']
).properties(
    title='Número de solicitações de pagamento por UF'
)

st.altair_chart(chart, use_container_width=True)
