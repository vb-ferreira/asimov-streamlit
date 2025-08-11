import streamlit as st
import pandas as pd

st.title('Sollicitações de pagamento')

# Data
df = st.session_state['df_leei']

# Tabela
st.dataframe(
  df,
  hide_index=True
)
