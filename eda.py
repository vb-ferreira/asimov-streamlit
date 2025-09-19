import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **Lendo os dados do Google Sheets**""")
    return


@app.cell
def _(pd):
    # ID da planilha google no Drive do projeto
    sheet_id = '1feQz1NCOBN3GEszFV4Ziqp7wOysMWe-bAjcLpUx2JXw'

    df_raw = pd.read_csv(
        f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=All',
        header=0,
        usecols=['ID', 'RELATÓRIO', 'FORMADOR', 'MUNICÍPIO', 'UF', 'TURMA','OFÍCIO', 'ENVIO'],
        dtype={'TURMA': str},
    )

    # Dispensa a primeira coluna
    df = df_raw.iloc[:, 1:]
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **Limpeza dos dados**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Deixa apenas o número na coluna `RELATÓRIO`.""")
    return


@app.cell
def _(df):
    df['RELATÓRIO'] = df['RELATÓRIO'].str.extract(r'(\d+)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Removendo a acentuação das colunas `FORMADOR` e `MUNCÍPIO`.""")
    return


@app.cell
def _(df):
    df['FORMADOR'] = df['FORMADOR'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df['MUNICÍPIO'] = df['MUNICÍPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Exclui o número da página no SIPAC (entre parênteses) da coluna `OFÍCIO`.""")
    return


@app.cell
def _(df):
    df['OFÍCIO'] = df['OFÍCIO'].str.extract(r'^(\d+)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Extrai o nº da turma da coluna `FORMADOR` para uma nova coluna.""")
    return


@app.cell
def _(df):

    # Extrai o número da turma da coluna "FORMADOR" para criar outra coluna
    df['TURMA Nº'] = df['FORMADOR'].str.extract(r'\((.a) TURMA\)')

    # Preenche os valores NaN com '1a'
    df['TURMA Nº'] = df['TURMA Nº'].fillna('1a TURMA')

    # Exclui o número da turma da coluna `FORMADOR`
    # df['FORMADOR'] = df['FORMADOR'].str.replace(r' \(\da TURMA\)', '', regex=True)

    # Exclui o termo "TURMA"" da coluna `TURMA Nº`
    df['TURMA Nº'] = df['TURMA Nº'].str.replace(' TURMA', '')
    return


@app.cell
def _(df):
    # Lista as colunas do seu DataFrame na ordem original
    colunas = list(df.columns)

    # Move a coluna 'TURMA Nº' para a terceira posição (índice 2)
    colunas.remove('TURMA Nº')
    colunas.insert(2, 'TURMA Nº')

    # DataFrame Final
    dff = df[colunas]
    return (dff,)


@app.cell
def _(dff):
    dff
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **Métricas**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Em um cópia do DataFrame, converte a **data de envio** em **índice**.""")
    return


@app.cell
def _(dff, pd):
    df_metrics = dff.copy()
    df_metrics['ENVIO'] = pd.to_datetime(df_metrics['ENVIO'], dayfirst=True)
    df_metrics.set_index('ENVIO', inplace=True)
    return (df_metrics,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Calcula **média semanal de solicitações**.""")
    return


@app.cell
def _(df_metrics):
    solicitacoes_semanais = df_metrics.resample('W').size().reset_index(name='Numero de Solicitacoes')

    numero_solicitacoes = solicitacoes_semanais['Numero de Solicitacoes'].sum()
    media_solicitacoes = round(solicitacoes_semanais['Numero de Solicitacoes'].mean(), 2) 

    print('Número de solicitações: ', numero_solicitacoes)
    print('Média semanal de solicitações: ', media_solicitacoes)
    return (numero_solicitacoes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Calcula **média semanal de ofícios**.""")
    return


@app.cell
def _(df_metrics):
    df_temp = df_metrics.reset_index()

    df_oficios_unicos = df_temp.drop_duplicates(subset=['OFÍCIO', 'ENVIO'])
    df_oficios_unicos.set_index('ENVIO', inplace=True)
    oficios_semanais = df_oficios_unicos.resample('W').size().reset_index(name='Numero de Oficios')

    numero_oficios = oficios_semanais['Numero de Oficios'].sum()
    media_oficios = round(oficios_semanais['Numero de Oficios'].mean(), 2)

    print('Número de ofícios: ', numero_oficios)
    print('Média semanal de ofícios: ', media_oficios)
    return (numero_oficios,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Calcula a **média de solicitações por ofício**.""")
    return


@app.cell
def _(numero_oficios, numero_solicitacoes):
    solicitacoes_por_oficio = round(numero_solicitacoes/numero_oficios, 2)
    print(solicitacoes_por_oficio)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **Funções Exportadas**""")
    return


@app.cell
def _(pd):
    def calc_solicitacoes(df):
        df_metrics = df.copy()
        df_metrics['ENVIO'] = pd.to_datetime(df_metrics['ENVIO'], dayfirst=True)
        df_metrics.set_index('ENVIO', inplace=True)

        solicitacoes_semanais = df_metrics.resample('W').size().reset_index(name='Numero de Solicitacoes')

        numero_solicitacoes = solicitacoes_semanais['Numero de Solicitacoes'].sum()
        media_solicitacoes = round(solicitacoes_semanais['Numero de Solicitacoes'].mean(), 2) 

        return (numero_solicitacoes, media_solicitacoes)
    return


@app.cell
def _(dff, pd):
    def calc_oficios():
        df_metrics = dff.copy()
        df_metrics['ENVIO'] = pd.to_datetime(df_metrics['ENVIO'], dayfirst=True)
        df_metrics.set_index('ENVIO', inplace=True)

        df_temp = df_metrics.reset_index()
        df_oficios_unicos = df_temp.drop_duplicates(subset=['OFÍCIO', 'ENVIO'])
        df_oficios_unicos.set_index('ENVIO', inplace=True)
        oficios_semanais = df_oficios_unicos.resample('W').size().reset_index(name='Numero de Oficios')

        numero_oficios = oficios_semanais['Numero de Oficios'].sum()
        media_oficios = round(oficios_semanais['Numero de Oficios'].mean(), 2)

        return (numero_oficios, media_oficios)
    return


if __name__ == "__main__":
    app.run()
