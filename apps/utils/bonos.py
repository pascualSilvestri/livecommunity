
def  bonoIndirecto(up_link,cpa):
    print(up_link.fpa,up_link.cpaIndirecto,up_link.cpa,up_link.level_bono_indirecto)
    if up_link.cpaIndirecto >= 5 and up_link.cpa >=2 and up_link.level_bono_indirecto == 0:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level1').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 10 and up_link.cpa >=3 and up_link.level_bono_indirecto == 1:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level2').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 20 and up_link.cpa >=4 and up_link.level_bono_indirecto == 2:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level3').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 30 and up_link.cpa >=5 and up_link.level_bono_indirecto == 3:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level4').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 50 and up_link.cpa >=6 and up_link.level_bono_indirecto == 4:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level5').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 100 and up_link.cpa >=7 and up_link.level_bono_indirecto == 5:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level6').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 150 and up_link.cpa >=8 and up_link.level_bono_indirecto == 6:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level7').valor)
        up_link.level_bono_indirecto += 1
        
    if up_link.cpaIndirecto >= 200 and up_link.cpa >=9 and up_link.level_bono_indirecto == 7:
        up_link.monto_bono_indirecto = int(cpa.objects.get(bono='level8').valor)
        up_link.level_bono_indirecto += 1


def bonoDirecto(usuario,cpa):
    if usuario.cpa== 5  and usuario.level_bono_directo == 0:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level1').valor)
        usuario.level_bono_directo += 1
    if usuario.cpa== 10  and usuario.level_bono_directo== 1:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level2').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 15  and usuario.level_bono_directo== 2:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level3').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 20  and usuario.level_bono_directo== 3:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level4').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 30  and usuario.level_bono_directo== 4:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level5').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 50  and usuario.level_bono_directo== 5:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level6').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 70  and usuario.level_bono_directo== 6:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level7').valor )
        usuario.level_bono_directo += 1
    if usuario.cpa== 100 and usuario.level_bono_directo== 7:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level8').valor)
        usuario.level_bono_directo += 1
    if usuario.cpa== 150 and usuario.level_bono_directo== 8:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level9').valor) 
        usuario.level_bono_directo += 1
    if usuario.cpa== 200 and usuario.level_bono_directo== 9:
        usuario.monto_bono_directo =int(cpa.objects.get(bono='level10').valor) 
        usuario.level_bono_directo += 1
    if  usuario.have_bono == True and usuario.cpa != 5 and usuario.cpa != 10 and usuario.cpa != 15 and usuario.cpa != 20 and usuario.cpa != 30 and usuario.cpa != 50 and usuario.cpa != 70 and usuario.cpa != 100 and usuario.cpa != 150 and usuario.cpa != 200:
        usuario.have_bono=False  

