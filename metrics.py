import pandas as pd

def calc_oficios(df):
    df_metrics = df.copy()
    df_metrics['ENVIO'] = pd.to_datetime(df_metrics['ENVIO'], dayfirst=True)
    df_metrics.set_index('ENVIO', inplace=True)

    df_temp = df_metrics.reset_index()
    df_oficios_unicos = df_temp.drop_duplicates(subset=['OFÍCIO', 'ENVIO'])
    df_oficios_unicos.set_index('ENVIO', inplace=True)
    oficios_semanais = df_oficios_unicos.resample('W').size().reset_index(name='Numero de Oficios')

    numero_oficios = oficios_semanais['Numero de Oficios'].sum()
    media_oficios = round(oficios_semanais['Numero de Oficios'].mean(), 2)

    return (numero_oficios, media_oficios)

def calc_solicitacoes(df):
    df_metrics = df.copy()
    df_metrics['ENVIO'] = pd.to_datetime(df_metrics['ENVIO'], dayfirst=True)
    df_metrics.set_index('ENVIO', inplace=True)

    solicitacoes_semanais = df_metrics.resample('W').size().reset_index(name='Numero de Solicitacoes')

    numero_solicitacoes = solicitacoes_semanais['Numero de Solicitacoes'].sum()
    media_solicitacoes = round(solicitacoes_semanais['Numero de Solicitacoes'].mean(), 2)

    return (numero_solicitacoes, media_solicitacoes)
