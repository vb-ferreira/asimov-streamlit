import streamlit as st
import pandas as pd

# Page config
def wide_space_default():
  st.set_page_config(layout='wide')

st.logo(
  'img/cnca-logo.png',
  size="large"
)

wide_space_default()

# Data
SHEET_ID = '1feQz1NCOBN3GEszFV4Ziqp7wOysMWe-bAjcLpUx2JXw'

@st.cache_data
def load_data(sheet_id):
  df_raw = pd.read_csv(
    f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=All',
    header=0,
    usecols=['ID', 'RELATÓRIO', 'FORMADOR', 'MUNICÍPIO', 'UF', 'TURMA','OFÍCIO', 'ENVIO'],
    dtype={'TURMA': str},
  )
  # Dispensa a primeira coluna
  df = df_raw.iloc[:, 1:]
  return df

@st.cache_data
def cleaning_data(df):
  df['RELATÓRIO'] = df['RELATÓRIO'].str.extract(r'(\d+)')
  df['FORMADOR'] = df['FORMADOR'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
  df['MUNICÍPIO'] = df['MUNICÍPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
  df['OFÍCIO'] = df['OFÍCIO'].str.extract(r'^(\d+)')
  df['TURMA Nº'] = df['FORMADOR'].str.extract(r'\((.a) TURMA\)')
  df['TURMA Nº'] = df['TURMA Nº'].fillna('1a TURMA')
  df['FORMADOR'] = df['FORMADOR'].str.replace(r' \(\da TURMA\)', '', regex=True)
  df['TURMA Nº'] = df['TURMA Nº'].str.replace(' TURMA', '')
  df['TURMA Nº'] = df['TURMA Nº'].str.replace('a', 'ª')
  colunas = list(df.columns)
  colunas.remove('TURMA Nº')
  colunas.insert(2, 'TURMA Nº')
  df = df[colunas]
  return df

if "df_leei" not in st.session_state:
  df = load_data(SHEET_ID)
  df = cleaning_data(df)
  st.session_state['df_leei'] = df

# Navigation
pages = [
  st.Page('app_pages/tabela.py', title='Tabela'),
  st.Page('app_pages/dashboard.py', title='Dashboard')
]

pg = st.navigation(pages, position='top')

pg.run()
