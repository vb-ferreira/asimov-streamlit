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
    # y=alt.Y('Category:N', sort=custom_order, title=''),  # 'N' para dados nominais/qualitativos
    # x=alt.X('Count:Q', title=''),                        # 'Q' para dados quantitativos
    y=alt.Y('Count:Q', title=''),  # 'N' para dados nominais/qualitativos
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
df_registros_counts['Solicitações'] = df_registros_counts['Número de Registros'].rolling(window=7, min_periods=1).mean()

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
    df_registros_counts[['Data de Envio', 'Solicitações']],
    df_oficios_counts[['Data de Envio', 'Ofícios']],
    on='Data de Envio',
    how='outer' # garante que nenhuma data seja perdida, mesmo se não houver ofício
).sort_values(by='Data de Envio').fillna(0) # preenche dias sem dados com 0

# O pd.melt() transformar o df para o formato "longo"
df_long = df_merged.melt(
    id_vars=['Data de Envio'],
    value_vars=['Solicitações', 'Ofícios'],
    var_name='Métrica',
    value_name='Valor da Média Móvel'
)

# Cria o gráfico de linhas com base no DataFrame 'df_long'
chart_3 = alt.Chart(df_long).mark_line(point=True).encode(
    x=alt.X('Data de Envio:T', axis=alt.Axis(format="%d/%m/%Y"), title=''),
    y=alt.Y('Valor da Média Móvel:Q', title=''),

    # O  'color' cria uma linha para cada valor único na coluna 'Métrica'.
    color=alt.Color(
        'Métrica:N',
        legend=alt.Legend(title='', orient='top-left'),
        scale=alt.Scale(domain=['Ofícios', 'Solicitações'], range=['orange', 'blue'])
        ),
    tooltip=[
        alt.Tooltip('Data de Envio:T', title='Data', format="%d/%m/%Y"),
        alt.Tooltip('Métrica:N', title='Métrica'),
        alt.Tooltip('Valor da Média Móvel:Q', title='Média', format=".2f") # Formata para 2 casas decimais
    ]
).properties(
    title={
        "text": "Número de solicitações por período",
        "fontSize": 24,
        "subtitle": "Média móvel semanal de solicitações vs. ofícios",
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
