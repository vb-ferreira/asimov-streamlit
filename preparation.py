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
    mo.md(r"""# **01 Lendo os dados do Google Sheets**""")
    return


@app.cell
def _(pd):
    sheet_id = '1feQz1NCOBN3GEszFV4Ziqp7wOysMWe-bAjcLpUx2JXw'
    df = pd.read_csv(
        f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=All',
        header=None,
        names=['#', 'RELATÓRIO', 'NOME', 'MUNICÍPIO', 'UF', 'TURMA', 'CONTRATO', 'OFÍCIO', 'DATA']
    )
    df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
