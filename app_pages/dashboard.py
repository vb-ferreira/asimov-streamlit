import streamlit as st
import pandas as pd
import altair as alt

# Data
df = st.session_state['df_leei']

# Solicitações por UF
frequency_series_uf = df['UF'].value_counts()

frequency_uf = frequency_series_uf.reset_index()
frequency_uf.columns = ['Category', 'Count']

chart_1 = alt.Chart(frequency_uf).mark_bar().encode(
    y=alt.Y('Category:N', title=''),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title=''),     # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title='Número de solicitações de pagamento por UF'
)

# Solicitações por Relatório
frequency_series_rel = df['RELATÓRIO'].value_counts()

frequency_rel = frequency_series_rel.reset_index()
frequency_rel.columns = ['Category', 'Count']

custom_order = ["RELATÓRIO 1", "RELATÓRIO 2", "RELATÓRIO 3", "RELATÓRIO 4", "RELATÓRIO 5",
                "RELATÓRIO 6", "RELATÓRIO 7", "RELATÓRIO 8", "RELATÓRIO 9", "RELATÓRIO 10"]

chart_2 = alt.Chart(frequency_rel).mark_bar().encode(
    y=alt.Y('Category:N', sort=custom_order, title=''),  # 'N' para dados nominais/qualitativos
    x=alt.X('Count:Q', title=''),     # 'Q' para dados quantitativos
    tooltip=['Category', 'Count']
).properties(
    title='Número de solicitações de pagamento por relatório'
)

# Solicitações por data (teste)

# Converte a coluna 'DATA' para `datetime`.
# O parâmetro 'dayfirst=True' é importante para interpretar o formato dd/mm/aaaa corretamente.
df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True)

# Agrupa os dados por data para contar o número de registros por dia.
df_counts = df['DATA'].value_counts().reset_index()
df_counts.columns = ['Data de Envio', 'Número de Registros']
df_counts = df_counts.sort_values(by='Data de Envio')

# Calcula a média móvel semanal (média dos últimos 7 dias).
df_counts['Média Móvel Semanal'] = df_counts['Número de Registros'].rolling(window=7).mean()

# Cria o gráfico de linhas com Altair
chart_3 = alt.Chart(df_counts).mark_line().encode(
    # Define o eixo X como a data de envio.
    x=alt.X('Data de Envio', axis=alt.Axis(format="%d/%m/%Y"), title='Data de Envio'),
    # Define o eixo Y como oa média móvel semanal.
    y=alt.Y('Média Móvel Semanal', title='Média Móvel Semanal'),
    # Adiciona tooltips para mostrar os valores ao passar o mouse.
    tooltip=[
        alt.Tooltip('Data de Envio', title='Data de Envio', format="%d/%m/%Y"),
        alt.Tooltip('Média Móvel Semanal', title='Média Móvel Semanal')
    ]
).properties(
    title='Número de solicitações por período'
).interactive() # Permite interação (zoom e pan) no gráfico.

# Plot
st.altair_chart(chart_1, use_container_width=True)
st.altair_chart(chart_2, use_container_width=True)
st.altair_chart(chart_3, use_container_width=True)
