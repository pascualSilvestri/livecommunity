

# def calcula_porcentaje_directo(valor,porcentaje,porcentaje_socio):
    
#     return ((valor*5/porcentaje)*porcentaje_socio)

def calcula_porcentaje_directo(valor,porcentaje,porcentaje_socio):
    
    return ((valor*100/porcentaje)*(porcentaje_socio/100))



def calcular_porcentaje_indirecto(valor,porcentaje_socio):
    return (valor*(porcentaje_socio/100))

