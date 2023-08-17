def existe(client,fecha_registro,fpa,status,fecha_calif,country,posicion_cuenta,fecha_primer_deposito,neto_deposito,numeros_depositos,registros):
    
    for r in registros:
        if(client==r.client and fecha_registro == r.fecha_registro and fpa == r.fpa and status ==  r.status and fecha_calif == r.fecha_calif and country == r.country and posicion_cuenta == r.posicion_cuenta and fecha_primer_deposito == r.fecha_primer_deposito and neto_deposito == r.neto_deposito and numeros_depositos == r.numeros_depositos):
            return True
    return False


def existe_cpa(fecha,monto,client,fpa,cpas):
    for c in cpas:
        if (fecha==c['fecha_creacion'] and monto == c['monto'] and client == c['client'] and fpa == c['fpa']):
            return True
    return False

def existe_ganancia(
    client,
    fpa,
    full_name,
    country,
    equity,
    balance,
    partner_earning,
    skilling_earning,
    skilling_markup,
    skilling_commission,
    volumen,
    fecha_last_trade,
    fecha_first_trade,
    closed_trade_count,
    customer_pnl,
    deposito_neto,
    deposito,
    withdrawals,
    ganancias):
    for g in ganancias:
        if (client == g['client'] and fpa == g['fpa'] and full_name == g['full_name'] and country == g['country'] and equity == g['equity'] and balance == g['balance'] and partner_earning == g['partner_earning'] and skilling_earning == g['skilling_earning'] and skilling_markup == g['skilling_markup'] and skilling_commission == g['skilling_commission'] and volumen == g['volumen'] and fecha_last_trade == g['fecha_last_trade'] and fecha_first_trade == g['fecha_first_trade'] and closed_trade_count == g['closed_trade_count'] and customer_pnl == g['customer_pnl'] and deposito_neto == g['deposito_neto'] and deposito == g['deposito'] and withdrawals == g['withdrawals']):
            return True
    return False


def formatera_retiro(valor):
    retiro = valor.replace('(','').strip()
    retiro = retiro.replace(')','').strip()
    retiro = retiro.split(' ')
    
    return retiro