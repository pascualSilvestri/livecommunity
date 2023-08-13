
def  bonoIndirecto(up_link,cpa):
    if up_link.cpaIndirecto >= 5 and up_link.cpa >=2 and up_link.level_bono_indirecto == 0:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA5').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 10 and up_link.cpa >=3 and up_link.level_bono_indirecto == 1:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA10').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 20 and up_link.cpa >=4 and up_link.level_bono_indirecto == 2:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA20').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 30 and up_link.cpa >=5 and up_link.level_bono_indirecto == 3:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA30').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 50 and up_link.cpa >=6 and up_link.level_bono_indirecto == 4:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA50').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 100 and up_link.cpa >=7 and up_link.level_bono_indirecto == 5:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA100').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 150 and up_link.cpa >=8 and up_link.level_bono_indirecto == 6:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA150').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 200 and up_link.cpa >=9 and up_link.level_bono_indirecto == 7:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='CPA200').valor)
        up_link.level_bono_indirecto += 1


def bonoDirecto(usuario,cpa):
    if usuario.cpa== 5  and usuario.level_bono_directo == 0:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='5CPA').valor)
        usuario.level_bono_directo += 1
    if usuario.cpa== 10  and usuario.level_bono_directo== 1:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='10CPA').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 15  and usuario.level_bono_directo== 2:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='15CPA').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 20  and usuario.level_bono_directo== 3:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='20CPA').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 30  and usuario.level_bono_directo== 4:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='30CPA').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 50  and usuario.level_bono_directo== 5:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='50CPA').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 70  and usuario.level_bono_directo== 6:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='70CPA').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 100 and usuario.level_bono_directo== 7:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='100CPA').valor)
        usuario.level_bono_directo += 1
    if usuario.cpa== 150 and usuario.level_bono_directo== 8:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='150CPA').valor) 
        usuario.level_bono_directo += 1
    if usuario.cpa== 200 and usuario.level_bono_directo== 9:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='200CPA').valor) 
        usuario.level_bono_directo += 1
    if  usuario.haveBono == True and usuario.cpa != 5 and usuario.cpa != 10 and usuario.cpa != 15 and usuario.cpa != 20 and usuario.cpa != 30 and usuario.cpa != 50 and usuario.cpa != 70 and usuario.cpa != 100 and usuario.cpa != 150 and usuario.cpa != 200:
        usuario.haveBono=False  

