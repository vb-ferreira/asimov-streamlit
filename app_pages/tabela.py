import streamlit as st
import pandas as pd

st.title('Sollicitações de pagamento')

df = st.session_state['df_leei']

st.dataframe(
  df,
  hide_index=True
)
