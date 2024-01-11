from ..skilling.models import Registros_ganancias

def existe(client,fecha_registro,fpa,status,fecha_calif,country,posicion_cuenta,fecha_primer_deposito,neto_deposito,numeros_depositos,registros):
    
    for r in registros:
        if(client==r.client and fecha_registro == r.fecha_registro and fpa == r.fpa and status ==  r.status and fecha_calif == r.fecha_calif and country == r.country and posicion_cuenta == r.posicion_cuenta and fecha_primer_deposito == r.fecha_primer_deposito and neto_deposito == r.neto_deposito and numeros_depositos == r.numeros_depositos):
            return True
    return False


def existe_cpa(fecha,monto,client,fpa,cpas):
    for c in cpas:
        if (fecha==c.fecha_creacion and monto == c.monto and client == c.client and fpa == c.fpa):
            return True
    return False

def existe_ganancia(ganancia: Registros_ganancias, ganancias: list) -> bool:
    g = ganancias.filter(
        client=ganancia.client,
        fpa=ganancia.fpa,
        partner_earning=ganancia.partner_earning,
        fecha_operacion=ganancia.fecha_operacion,
        deal_id=ganancia.deal_id,
        position=ganancia.position
    )
    
    if g.exists():
        return True
    else:
        return False

def formatera_retiro(valor):
    retiro = valor.replace('(','').strip()
    retiro = retiro.replace(')','').strip()
    retiro = retiro.split(' ')
    
    return retiro