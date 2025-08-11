import streamlit as st
import pandas as pd

# Data
@st.cache_data
def load_data():
  df = pd.read_csv(
    "leei.csv",
    header=None,
    names=['#', 'RELATÓRIO', 'NOME', 'MUNICÍPIO', 'UF', 'TURMA', 'CONTRATO', 'OFÍCIO', 'DATA'],
  )
  return df

df = load_data()
st.session_state['df_leei'] = df

# Navigation
pages = [
  st.Page('app_pages/tabela.py', title='Tabela'),
  st.Page('app_pages/dashboard.py', title='Dashboard')
]

pg = st.navigation(pages, position='sidebar')

pg.run()
