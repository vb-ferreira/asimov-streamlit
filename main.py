import streamlit as st
import pandas as pd

# Page config
def wide_space_default():
  st.set_page_config(layout='wide')

wide_space_default()

# Data
@st.cache_data
def load_data():
  df = pd.read_csv(
    "leei.csv",
    header=None,
    names=['#', 'RELATÓRIO', 'NOME', 'MUNICÍPIO', 'UF', 'TURMA', 'CONTRATO', 'OFÍCIO', 'DATA'],
  )
  return df

if "df_leei" not in st.session_state:
  df = load_data()
  st.session_state['df_leei'] = df

# Navigation
pages = [
  st.Page('app_pages/tabela.py', title='Tabela'),
  st.Page('app_pages/dashboard.py', title='Dashboard')
]

pg = st.navigation(pages, position='top')

pg.run()
