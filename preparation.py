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


if __name__ == "__main__":
    app.run()
