import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title('Solicitações de pagamento')

# Data
df = st.session_state['df_leei']

# AgGrid
tabBasico, tabAgrupado = st.tabs(['Dados Brutos', 'Dados Agregados'])

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

  gob.configure_column('#', header_name="#", width=75, filter=False)
  gob.configure_column('RELATÓRIO', header_name="RELATÓRIO", filter=True)
  gob.configure_column('NOME', header_name="NOME", filter=True)
  gob.configure_column('MUNICÍPIO', header_name="MUNICÍPIO", filter=True)
  gob.configure_column('UF', header_name="UF", width=100, filter=True)
  gob.configure_column('DATA', header_name="DATA", filter=True)

  gridOptions = gob.build()

  AgGrid(
    df,
    gridOptions=gridOptions,
    height=500,
    width='100%',
    theme='material',
    fit_columns_on_grid_load=True
  )

with tabAgrupado:
  st.write('Em desenvolvimento')
