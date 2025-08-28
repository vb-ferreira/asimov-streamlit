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
    mo.md(r"""# **1 Series**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Criando Series** a partir de **listas**.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Series** guardam tipos de **dados homogêneos** (se a lista tiver dados heterogêneos, estes serão convertidos para um mesmo tipo).""").callout()
    return


@app.cell
def _(pd):
    idades = [16, 16, 42, 42, 43, 75]

    idades_sr = pd.Series(idades)

    print(idades_sr)
    return (idades_sr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A classe [pandas.Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html) possui diversos **métodos** e atributos, muitos deles úteis para a **estatística descritiva**.""")
    return


@app.cell
def _(idades_sr):
    # média
    idades_sr.mean()
    return


@app.cell
def _(idades_sr):
    # variância
    idades_sr.var()
    return


@app.cell
def _(idades_sr):
    # desvio padrão
    idades_sr.std()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **2 Seleção com `iloc` | `loc`**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Os **índices das Series** funcionam da mesma maneira que as **chaves dos dicionários**, com a diferença que nas **Series**, ele pode se **repetir**. Logo, geralmente **não é recomendado acessar** seus elementos pelo **índice** com a notação de colchetes, uma vez que isto pode retornar um ou vários valores.""").callout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Para acessar um valor por sua **posição**, use o [pandas.Series.iloc]([http://](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.iloc.html)).""")
    return


@app.cell
def _(idades_sr):
    # Último item de uma Series
    idades_sr.iloc[-1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""O [pandas.Series.loc]([http://](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.loc.html)) faz a seleção pelo **índice (label)**. Ou seja, da forma mesma forma que `lista[índice]`. Faz mais sentido quando usado em **DataFrames**.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **DataFrames** são **coleções de Series**, organizadas em **colunas**.

    Ao acessar uma **coluna** com `df[column_name]` é retornada uma Series, cujos **índices são os índices do DataFrame**.

    Ao acessar uma **linha** com `df.iloc[position]` também é retornada um Series, mas os **índices são os nomes das colunas**.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **3 Importação de dados**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Um dos formatos mais comuns de arquivo é o **csv**. O método [pandas.read_csv]([http://](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)) possui **diversos argumentos** para configurarmos a leitura desse tipo de arquivo.""")
    return


@app.cell
def _(pd):
    df_clientes = pd.read_csv('datasets/clientes.csv', delimiter=';')
    df_clientes.head()
    return (df_clientes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **4 Dataframes**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Exibindo as 5 **primeiras linhas** do DataFrame.""")
    return


@app.cell
def _(df_clientes):
    df_clientes.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Exibindo as 3 **últimas linhas** do DataFrame.""")
    return


@app.cell
def _(mo):
    mo.md(r"""df_clientes.tail(3)""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Amostra aleatória** do DataFrame.""")
    return


@app.cell
def _(df_clientes):
    df_clientes.sample(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Exibindo as **dimensões** do DataFrame com o atributo `shape` (retorna uma **tupla**).""")
    return


@app.cell
def _(df_clientes):
    df_clientes.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""O atributo `dtypes` retorna os **tipos de dados** das colunas em uma `Series`.""")
    return


@app.cell
def _(df_clientes):
    df_clientes.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Para mais **conteúdo introdutório** veja o artigo [10 minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html), da própria documentação.""").callout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## **Renomeando colunas**""")
    return


@app.cell
def _(pd):
    df_transacoes = pd.read_csv('datasets/transacoes.csv', delimiter=';')
    df_transacoes.columns
    return (df_transacoes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Renomeando** uma coluna:""")
    return


@app.cell
def _(df_transacoes):
    df_transacoes.rename(columns={'QtdePontos': 'qtPontos'}).columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Por padrão, o argumento `inplace` é `False`, o que significa que o `rename` **retorna um novo DataFrame** ao invés de modificar o original.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// details | Explicação do código
        type: info

    **`[1]`**: `{'Nome antigo': 'Nome novo'}`<br>
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Para **reordenar** as colunas, basta selecioná-las com a nova ordem.""")
    return


@app.cell
def _(df_transacoes):
    ordem_alfabetica = df_transacoes.columns.sort_values()
    df_ordered_columns = df_transacoes[ordem_alfabetica]
    return (df_ordered_columns,)


@app.cell
def _(df_ordered_columns):
    df_ordered_columns.columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **5 Filtros**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""DataFrame **transações**:""")
    return


@app.cell(hide_code=True)
def _(df_transacoes):
    df_transacoes.head(1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""DataFrame **Clientes**:""")
    return


@app.cell(hide_code=True)
def _(df_clientes):
    df_clientes.head(1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Q1**: Quais transações têm mais de 50 pontos?""")
    return


@app.cell
def _(df_transacoes):
    q1_mask = df_transacoes['QtdePontos'] > 50
    df_transacoes[q1_mask].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// details | Explicação do código
        type: info

    **[1]**: É criada um Series de booleanos com as mesmas dimensões da estrutura original. Usaremos essa Series para filtrar o DataFrame, técnica conhecida como **boolean indexing**.<br>
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Q2**: Quais transações têm 50 ou mais e menos de 100 pontos?""")
    return


@app.cell
def _(df_transacoes):
    q2_mask = (df_transacoes['QtdePontos'] >= 50) & (df_transacoes['QtdePontos'] < 100)
    df_transacoes[q2_mask].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// details | Explicação do código
        type: info

    **[1]**: Os **parênteses** aqui são **obrigatórios** devido a maior precedência do operador bitwise `&` sobre os operadores de comparação `>=` e `<`.<br>
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Q3**: Quais transações são do sistema "twitch" ou "cursos"?""")
    return


@app.cell
def _(df_transacoes):
    q3_mask = df_transacoes['DescSistemaOrigem'].isin(['twitch', 'cursos'])
    df_transacoes[q3_mask].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Q4**: Quais clientes têm a data de criação registrada (não nula)?""")
    return


@app.cell
def _(df_clientes):
    q4_mask = df_clientes['DtCriacao'].notna()
    df_clientes[q4_mask].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **6 Novas colunas e ordenação**""")
    return


@app.cell(hide_code=True)
def _(df_clientes):
    df_clientes.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Criando **nova coluna**:""")
    return


@app.cell
def _(df_clientes):
    df_clientes['pontos_100'] = df_clientes['QtdePontos'] + 100
    return


@app.cell
def _(df_clientes):
    df_clientes.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Ordenando** o DataFrame pelos valores de uma coluna:""")
    return


@app.cell
def _(df_clientes):
    df_clientes.sort_values(by='QtdePontos').tail()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A **ordenação** pode ser feita por **mais de uma coluna**:""")
    return


@app.cell
def _(df_clientes):
    df_clientes.sort_values(by=['QtdePontos', 'DtCriacao'], ascending=[True, False]).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **7 `astype` | `replace`**""")
    return


if __name__ == "__main__":
    app.run()
