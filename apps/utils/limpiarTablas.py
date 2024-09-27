from datetime import datetime
import pandas as pd


def limpiar_datos_fpa(dataFrame):

    column_mapping = {
        'reporting.onboarding.customerId': 'id_client',
        'reporting.onboarding.customerFullName': 'full_name',
        'reporting.onboarding.country': 'country',
        'reporting.onboarding.registrationDate': 'fecha_registro',
        'reporting.onboarding.realAccountCreationDate': 'fecha_creacion_cuenta',
        'reporting.onboarding.verificationDate': 'verificacion',
        'reporting.onboarding.onboardingStatus': 'status',
        'reporting.onboarding.utmCampaign': 'fpa',
        'reporting.onboarding.utmContent': 'utm_content',
        'reporting.onboarding.utmTerm': 'utm_term'
    }

    dataFrame.rename(columns=column_mapping, inplace=True)
    
    getData = dataFrame[['id_client','fpa','full_name','country','fecha_registro','fecha_creacion_cuenta','verificacion','status']]
    # getData = getData[~getData['fpa'].str.contains('none', case=False)]
    return getData.to_dict(orient='records')


def limpiar_registros(dataframe):
    new_columns = {
        'User ID':'client',
        'Registration Date':'fecha_registro',
        'afp':'fpa',
        'Status':'status',
        'Qualification Date':'fecha_calif',
        'Country':'country',
        'Position Count':'posicion_cuenta',
        'Volume':'volumen',
        'First Deposit':'primer_deposito',
        'First Deposit Date':'fecha_primer_deposito',
        'Net Deposits':'neto_deposito',
        'Deposit Count':'numeros_depositos',
        'Commission':'comision'
    }
    dataframe.rename(columns=new_columns, inplace=True)
    #formatear fecha
    dataframe["fecha_registro"] = pd.to_datetime(dataframe["fecha_registro"]).dt.date
    dataframe["fecha_primer_deposito"] = pd.to_datetime(dataframe["fecha_primer_deposito"]).dt.date
    dataframe["fecha_calif"] = pd.to_datetime(dataframe["fecha_calif"]).dt.date

    # Reemplazar "skilling-" en la columna 'client'
    dataframe['client'] = dataframe['client'].str.replace('skilling-', '')

    # Rellenar NaN y NaT con 'none' en columnas seleccionadas
    columns_to_fill = ['fecha_registro', 'fpa', 'country', 'fecha_primer_deposito','fecha_calif']
    dataframe[columns_to_fill] = dataframe[columns_to_fill].fillna('none')
    dataframe = dataframe[dataframe['client'] != 'TOTAL']

    return dataframe.to_dict(orient='records')


def limpiar_cpa(dataframe):
    new_columns = {
        'created':'fecha_creacion',
        'amount':'monto', 
        'Commission_Type':'cpa', 
        'User_Id':'client', 
        'AFP':'fpa'
    }
    dataframe.rename(columns=new_columns, inplace=True)
    
    # Filtrar las filas con el valor "TOTAL"
    dataframe = dataframe[dataframe['fecha_creacion'] != 'TOTAL']
    
    # Usar .loc para asignar valores a la columna fecha_creacion
    dataframe.loc[:, "fecha_creacion"] = pd.to_datetime(dataframe["fecha_creacion"]).dt.date
    
    # Usar .loc para reemplazar 'skilling-' en la columna client
    dataframe.loc[:, 'client'] = dataframe['client'].str.replace('skilling-', '')

    return dataframe.to_dict(orient='records')


def limpiar_ganacias(dataFrame):
    column_mapping = {
        'Customer ID': 'client',
        'Position ID': 'position',
        'Symbol': 'symbol',
        'Direction': 'direccion',
        'Volume Traded (units)': 'volumen_trader',
        'Volume (USD)': 'volumne',
        'Trade date': 'fecha_operacion',
        'Trade Time (GMT)': 'hora_operacion',
        'Realized PnL': 'pnl',
        'Platform': 'plataforma',
        'Partner Earnings (USD)': 'partner_earning',
        'Deal ID': 'deal_id'
    }

    dataFrame.rename(columns=column_mapping, inplace=True)
    dataFrame = dataFrame[['client', 'position', 'symbol', 'fecha_operacion', 'partner_earning', 'deal_id']]
    return dataFrame.to_dict(orient='records')
