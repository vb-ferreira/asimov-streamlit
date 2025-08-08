import streamlit as st
import pandas as pd

# Read the CSV with new headers
df = pd.read_csv(
  "leei.csv",
  header=None,
  names=['#', 'RELATÓRIO', 'NOME', 'MUNICÍPIO', 'UF', 'TURMA', 'CONTRATO', 'OFÍCIO', 'DATA'],
)
st.dataframe(df, hide_index=True)
