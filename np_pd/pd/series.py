import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**[Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html)** é uma das **estruturas de dados fundamentais do Pandas**. É essencialmente um **array com um índice**. Por ser um array, todos os valores em uma série devem ser do **mesmo tipo**.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **Criando Series**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## **Criando Series a partir de listas**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Essa é a forma mais **simples** de criar uma Series.""")
    return


@app.cell
def _(pd):
    s1 = pd.Series([5, 10, 15, 20, 25, 30, 35])
    print(s1)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
