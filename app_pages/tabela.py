import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import webbrowser
import unicodedata

st.title('Solicitações de pagamento')

# Data
df = st.session_state['df_leei']

# AgGrid
tabBasico, tabAgrupado = st.tabs(['Dados Brutos', 'Dados Agregados'])

# Helper function to ignore accents and case on filter (?)
def to_lower_without_accents(value):
  if value is None:
    return None
  return unicodedata.normalize('NFD', value.lower()).encode('ascii', 'ignore').decode('utf-8')

with tabBasico:
  gob = GridOptionsBuilder.from_dataframe(df)

  gob.configure_default_column(
    groupable=True,
    value=True,
    enableRowGroup=True,
    aggFunc='sum',
  )

  gob.configure_pagination(paginationAutoPageSize=True)

  gob.configure_grid_options(
    suppressAggFuncInHeader=True,
    autoGroupColumnDef={'cellRendererParams': {'suppressCount': True}},
    pivotPanelShow='onlyWhenPivoting'
  )

  gob.configure_side_bar()
  gob.configure_pagination()

  gob.configure_column('RELATÓRIO', header_name="RELATÓRIO", filter=True)
  gob.configure_column('FORMADOR', header_name="FORMADOR", filter=True, width=500)
  gob.configure_column('TURMA Nº', header_name="TURMA Nº", filter=True)
  gob.configure_column('MUNICÍPIO', header_name="MUNICÍPIO", filter=True)
  gob.configure_column('UF', header_name="UF", filter=True, width=125)
  gob.configure_column('TURMA', header_name="TURMA", filter=False, width=145)
  gob.configure_column('OFÍCIO', header_name="OFÍCIO", filter=False, width=125)
  gob.configure_column('ENVIO', header_name="ENVIO", filter=True)

  gridOptions = gob.build()

  AgGrid(
    df,
    gridOptions=gridOptions,
    height=1000,
    width='100%',
    theme='material',
    fit_columns_on_grid_load=True,
    columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE
  )

with tabAgrupado:
  st.write('Em desenvolvimento')

# Link externo
btn = st.button('Open in Google Sheets')
if btn:
  webbrowser.open_new_tab('https://docs.google.com/spreadsheets/d/1feQz1NCOBN3GEszFV4Ziqp7wOysMWe-bAjcLpUx2JXw/edit?gid=887807750#gid=887807750')
