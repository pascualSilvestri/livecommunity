def existe(client,fecha_registro,fpa,status,fecha_calif,country,posicion_cuenta,fecha_primer_deposito,neto_deposito,numeros_depositos,registros):
    
    for r in registros:
        if(client==r.client and fecha_registro == r.fecha_registro and fpa == r.fpa and status ==  r.status and fecha_calif == r.fecha_calif and country == r.country and posicion_cuenta == r.posicion_cuenta and fecha_primer_deposito == r.fecha_primer_deposito and neto_deposito == r.neto_deposito and numeros_depositos == r.numeros_depositos):
            return True
    return False