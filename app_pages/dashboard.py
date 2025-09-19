import streamlit as st
import pandas as pd
import altair as alt
import locale
from metrics import calc_solicitacoes, calc_oficios

# DATA
df = st.session_state['df_leei']

df['ENVIO'] = pd.to_datetime(df['ENVIO'], dayfirst=True)

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') # Para Linux/macOS
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8') # Outra variação
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'portuguese_brazil') # Para Windows
        except locale.Error:
            print("Nenhum locale para português do Brasil foi encontrado.")

# MÉTRICAS
primeiro_dia = df['ENVIO'].min().strftime('%B/%Y')
ultimo_dia = df['ENVIO'].max().strftime('%B/%Y')

n_solicitacoes, media_solicitacoes = calc_solicitacoes(df)
n_oficios, media_oficios = calc_oficios(df)

solicitacoes_por_oficio = round(n_solicitacoes / n_oficios, 2)

# CHARTS

# Solicitações por UF
frequency_series_uf = df['UF'].value_counts()

frequency_uf = frequency_series_uf.reset_index()
frequency_uf.columns = ['Category', 'Count']

chart_1 = alt.Chart(frequency_uf).mark_bar().encode(
    y=alt.Y('Category:N', title=''),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title=''),     # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title={
        'text': 'Número de solicitações de pagamento por UF',
        'fontSize': 24,
        'subtitle': f'({primeiro_dia} - {ultimo_dia})',
        'subtitleFontSize': 16,
        'subtitleColor': 'gray'
    },
    height=350
)

# Solicitações por Relatório
frequency_series_rel = df['RELATÓRIO'].value_counts()

frequency_rel = frequency_series_rel.reset_index()
frequency_rel.columns = ['Category', 'Count']

custom_order = ["RELATÓRIO 1", "RELATÓRIO 2", "RELATÓRIO 3", "RELATÓRIO 4", "RELATÓRIO 5",
                "RELATÓRIO 6", "RELATÓRIO 7", "RELATÓRIO 8", "RELATÓRIO 9", "RELATÓRIO 10"]

chart_2 = alt.Chart(frequency_rel).mark_bar().encode(
    y=alt.Y('Count:Q', title=''),
    x=alt.X('Category:N', sort=custom_order, title='', axis=alt.Axis(labelAngle=0)),                        # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title={
        'text': 'Número de solicitações de pagamento por relatório',
        'fontSize': 24,
        'subtitle': f'({primeiro_dia} - {ultimo_dia})',
        'subtitleFontSize': 16,
        'subtitleColor': 'gray'
    },
    height=350
)

# Solicitações/ofícios por período
df['ENVIO'] = pd.to_datetime(df['ENVIO'], dayfirst=True)

# Contagem de solicitações por dia
df_registros_counts = df['ENVIO'].value_counts().reset_index()
df_registros_counts.columns = ['Data de Envio', 'Número de Registros']
df_registros_counts = df_registros_counts.sort_values(by='Data de Envio')

# Média móvel das solicitações
df_registros_counts['Relatórios'] = df_registros_counts['Número de Registros'].rolling(window=7, min_periods=1).mean()

# Ofícios únicos
df_oficios_unicos = df.drop_duplicates(subset=['OFÍCIO', 'ENVIO'])

# Contagem de ofícios únicos
df_oficios_counts = df_oficios_unicos['ENVIO'].value_counts().reset_index()
df_oficios_counts.columns = ['Data de Envio', 'Número de Ofícios']
df_oficios_counts = df_oficios_counts.sort_values(by='Data de Envio')

# Média móvel dos ofícios únicos
df_oficios_counts['Ofícios'] = df_oficios_counts['Número de Ofícios'].rolling(window=7, min_periods=1).mean()

# Concatena os dataframes
df_merged = pd.merge(
    df_registros_counts[['Data de Envio', 'Relatórios']],
    df_oficios_counts[['Data de Envio', 'Ofícios']],
    on='Data de Envio',
    how='outer' # garante que nenhuma data seja perdida, mesmo se não houver ofício
).sort_values(by='Data de Envio').fillna(0) # preenche dias sem dados com 0

# O pd.melt() transformar o df para o formato "longo"
df_long = df_merged.melt(
    id_vars=['Data de Envio'],
    value_vars=['Relatórios', 'Ofícios'],
    var_name='Métrica',
    value_name='Valor da Média Móvel'
)

# Radio button: as opções são os valores únicos da coluna 'Métrica'.
lista_de_metricas = df_long['Métrica'].unique()

# Se 'metrica_selecionada' ainda não existir na memória, definimos a primeira da lista como padrão.
if 'metrica_selecionada' not in st.session_state:
    st.session_state.metrica_selecionada = lista_de_metricas[0]

# Título dinâmico usando operador ternário
metrica_atual = st.session_state.metrica_selecionada

titulo_grafico = (
    "Ofícios"
    if metrica_atual == 'Ofícios'
    else "Relatórios"
)

# Filtrar o df com base na seleção ---
df_filtrado = df_long[df_long['Métrica'] == st.session_state.metrica_selecionada]

chart_3 = alt.Chart(df_filtrado).mark_line(
    point=True,
    strokeWidth=3
).encode(
    x=alt.X('Data de Envio:T', axis=alt.Axis(format="%d/%m/%Y"), title=''),
    y=alt.Y('Valor da Média Móvel:Q', title='', scale=alt.Scale(zero=False)),
    tooltip=[
        alt.Tooltip('Data de Envio:T', title='Data', format="%d/%m/%Y"),
        alt.Tooltip('Valor da Média Móvel:Q', title='Média', format=".2f")
    ]
).properties(
    # O título é dinâmico, baseado na seleção
    title={
        "text": f"{titulo_grafico} enviados para pagamento por período",
        "fontSize": 24,
        "subtitle": "Média móvel semanal",
        "subtitleFontSize": 16,
        "subtitleColor": "gray"
    }
).interactive()

# PLOT

# Cards
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Solicitações por semana", media_solicitacoes, border=True)
m2.metric("Ofícios por semana", media_oficios, border=True)
m3.metric("Total de solicitações", n_solicitacoes, border=True)
m4.metric("Total de ofícios", n_oficios, border=True)
m5.metric("Solicitações por ofício", solicitacoes_por_oficio, border=True)

st.divider()

# Charts
col1, col2 = st.columns(2, gap="large")

with col1:
    st.altair_chart(chart_1, use_container_width=True)

with col2:
    st.altair_chart(chart_2, use_container_width=True)

st.altair_chart(chart_3, use_container_width=True)

# Widget para seleção de métrica (Ofícios, Relatórios)
st.radio(
    label="",
    options=lista_de_metricas,
    key='metrica_selecionada',
    horizontal=True
)
