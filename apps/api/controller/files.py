from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...utils.limpiarTablas import limpiar_datos_fpa, limpiar_registros,limpiar_cpa,limpiar_ganacias
from ...utils.funciones import existe,existe_cpa,existe_ganancia
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...utils.bonos import bonoDirecto,bonoIndirecto
from ..models import Relation_fpa_client,Registro_archivo,Registros_cpa,Registros_ganancias
from ...usuarios.models import Cuenta,Usuario,Spread,BonoCpa,BonoCpaIndirecto
from datetime import datetime
import pandas as pd
import os


@csrf_exempt
def upload_fpa(request):
    if request.method == "POST" and request.FILES.get("csvFileFpa"):
        try:
            fpas = Relation_fpa_client.objects.all()
            csv_file = request.FILES["csvFileFpa"]
            file_name = csv_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[
                1
            ]  # obtengo la extencion del archivo

            if file_extension == ".csv":
                file_data = pd.read_csv(
                    csv_file, encoding="utf-8"
                )  # obtengo los datos de larchivo

                data_limpia = limpiar_datos_fpa(file_data)
                # print(data_limpia)
                for data in data_limpia:
                    # print(type(data['id_client']))
                    fecha_registro_string = str(data["fecha_registro"])
                    if fecha_registro_string == "nan":
                        fecha_registro = None
                    else:
                        fecha_registro = datetime.strptime(
                            fecha_registro_string, "%Y-%m-%d"
                        ).date()

                    fecha_creacion_string = str(data["fecha_creacion_cuenta"])
                    if fecha_creacion_string == "nan":
                        fecha_creacion = None
                    else:
                        fecha_creacion = datetime.strptime(
                            fecha_creacion_string, "%Y-%m-%d"
                        ).date()

                    fecha_verificacion_string = str(data["verificacion"])
                    if fecha_verificacion_string == "nan":
                        fecha_verificacion = None
                    else:
                        fecha_verificacion = datetime.strptime(
                            fecha_verificacion_string, "%Y-%m-%d"
                        ).date()

                    newData = Relation_fpa_client(
                        fpa=data["fpa"],
                        client=data["id_client"],
                        full_name=data["full_name"],
                        country=data["country"],
                        fecha_registro=fecha_registro,
                        fecha_creacion=fecha_creacion,
                        fecha_verificacion=fecha_verificacion,
                        status=data["status"],
                    )
                    montos= Cuenta(fpa=data["fpa"])
                    try:
                        f = Cuenta.objects.filter(fpa=data["fpa"])
                        if not f.exists():
                            montos.save()
                        fpa = fpas.filter(fpa=data["fpa"], client=data["id_client"])
                        if not fpa.exists():
                            newData.save()
                            
                    except Exception as e:
                        print(e)

            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"ErrorMessege": "Document is not format"})
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Salto la exception"})
        print("message Archivo CSV recibido y procesado exitosamente.")
        return JsonResponse(
            {"message": "Archivo CSV recibido y procesado exitosamente."}
        )
    else:
        print("error Se esperaba un archivo CSV en la solicitud POST.")
        return JsonResponse(
            {"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400
        )

@csrf_exempt
def upload_registros(request):
    if request.method == "POST" and request.FILES.get("csvFileRegistro"):
        try:
            fpas = Relation_fpa_client.objects.all()
            registros=Registro_archivo.objects.all()
            excel_file = request.FILES["csvFileRegistro"]
            file_name = excel_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo
            
            
            if file_extension == ".xlsx":
                
                file_data = pd.read_excel(excel_file,engine='openpyxl')  # obtengo los datos de larchivo
                new_data=limpiar_registros(file_data)
                
                for data in new_data:
                    fpa_id = fpas.filter(client=data['client'])
                    if fpa_id.exists():
                        fpa = fpa_id[0].fpa
                    else:
                        fpa = None
                    
                    fecha_registro_string = str(data["fecha_registro"])
                    if fecha_registro_string == "none":
                        fecha_registro = None
                    else:
                        fecha_registro = datetime.strptime(
                            fecha_registro_string, "%Y-%m-%d"
                        ).date()
                    
                    fecha_calif_string = str(data["fecha_calif"])
                    if fecha_calif_string == "none":
                        fecha_calif = None
                    else:
                        fecha_calif = datetime.strptime(
                            fecha_calif_string, "%Y-%m-%d"
                        ).date()
                    
                    fecha_primer_deposito_string = str(data["fecha_primer_deposito"])
                    if fecha_primer_deposito_string == "none":
                        fecha_primer_deposito = None
                    else:
                        fecha_primer_deposito = datetime.strptime(
                            fecha_primer_deposito_string, "%Y-%m-%d"
                        ).date()
                    
                    registro = Registro_archivo(
                        client= data['client'],
                        fecha_registro= fecha_registro,
                        fpa= fpa,
                        status= data['status'],
                        fecha_calif=fecha_calif,
                        country= data['country'],
                        posicion_cuenta= data['posicion_cuenta'],
                        volumen= data['volumen'],
                        primer_deposito= data['primer_deposito'],
                        fecha_primer_deposito=fecha_primer_deposito,
                        neto_deposito= data['neto_deposito'],
                        numeros_depositos= data['numeros_depositos'],
                        comision= data['comision'],
                    )
                    
                    if not existe(data['client'],fecha_registro,fpa,data['status'],fecha_calif,data['country'],data['posicion_cuenta'],fecha_primer_deposito,data['neto_deposito'],data['numeros_depositos'],registros):
                        registro.save()

                
            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"ErrorMessege": "Document is not format"},status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Salto la exception"},status=400)
        print("message Archivo CSV recibido y procesado exitosamente.")
        return JsonResponse(
            {"message": "Archivo CSV recibido y procesado exitosamente."}
        )
    else:
        print("error Se esperaba un archivo CSV en la solicitud POST.")
        return JsonResponse(
            {"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400
        )

@csrf_exempt
def upload_cpa(request):
    if request.method == "POST" and request.FILES.get("csvFileCpa"):
        try:
            fpas = Relation_fpa_client.objects.all()
            cpas = Registros_cpa.objects.all()
            excel_file = request.FILES["csvFileCpa"]
            file_name = excel_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo

            if file_extension == ".xlsx":
                file_data = pd.read_excel(excel_file,engine='openpyxl')  # obtengo los datos de larchivo
                new_data= limpiar_cpa(file_data)
                
                    
                for cpa in new_data:
                    fpa_id = fpas.filter(client=cpa['client']).first()
                    if fpa_id:
                        fpa = fpa_id.fpa
                    else:
                        fpa = None

                    fecha_creacion_string = str(cpa["fecha_creacion"])
                    if fecha_creacion_string == "none":
                        fecha_creacion = None
                    else:
                        fecha_creacion = datetime.strptime(
                            fecha_creacion_string, "%Y-%m-%d"
                        ).date()
                        
                    new_cpa = Registros_cpa(
                        fecha_creacion= fecha_creacion,
                        monto= cpa['monto'],
                        cpa= cpa['cpa'],
                        client= cpa['client'],
                        fpa= fpa
                    )
                    
                    
                    if not existe_cpa(fecha_creacion,cpa['monto'],cpa['client'],cpa['fpa'],cpas):
                        bono_directo = BonoCpa
                        bono_indirecto = BonoCpaIndirecto
                        cuenta = Cuenta.objects.filter(fpa=fpa)[0]
                        
                        if cuenta.fpa != 'none':
                            
                            usuario_up_line = Usuario.objects.filter(fpa=fpa)
                            if usuario_up_line.exists():
                                cuenta_up_line = Cuenta.objects.filter(fpa=usuario_up_line.first().uplink)
                            else:
                                cuenta_up_line = None
                            cuenta.monto_cpa += cpa['monto']
                            cuenta.cpa += 1
                            
                            bonoDirecto(cuenta,bono_directo)
                            if cuenta_up_line != None:
                                if cuenta_up_line.exists() :
                                    cuenta_up = cuenta_up_line.first()
                                    cuenta_up.cpaIndirecto += 1
                                    print(f'hijo: {usuario_up_line[0].fpa} padre: {cuenta_up_line[0].fpa}')
                                    bonoIndirecto(cuenta_up,bono_indirecto)
                                    cuenta_up.save()
                            new_cpa.save()
                            cuenta.save()
                            # usuario_up_line[0].save()
                                    
                            
                    
            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"ErrorMessege": "Document is not format"})
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Salto la exception"})
        print("message Archivo CSV recibido y procesado exitosamente.")
        return JsonResponse(
            {"message": "Archivo CSV recibido y procesado exitosamente."}
        )
    else:
        print("error Se esperaba un archivo CSV en la solicitud POST.")
        return JsonResponse(
            {"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400
        )

@csrf_exempt
def upload_ganancias(request):
    if request.method == "POST" and request.FILES.get("csvFileGanancias"):
        try:
            fpas = Relation_fpa_client.objects.all()
            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            excel_file = request.FILES["csvFileGanancias"]
            file_name = excel_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo

            if file_extension == ".csv":
                file_data = pd.read_csv(excel_file)  # obtengo los datos de larchivo
                new_data= limpiar_ganacias(file_data)
                
                for g in new_data:
                    fpa_id = fpas.filter(client=int(g['client']))
                    if fpa_id.exists():
                        fpa = fpa_id[0].fpa
                    else:
                        fpa = None
                    
                    fecha_first_trade_string = str(g["fecha_first_trade"])
                    if fecha_first_trade_string == "nan":
                        fecha_first_trade = None
                    else:
                        fecha_first_trade = datetime.strptime(
                            fecha_first_trade_string, "%Y-%m-%d"
                        ).date()
                    
                    fecha_last_trade_string = str(g["fecha_last_trade"])
                    if fecha_last_trade_string == "nan":
                        fecha_last_trade = None
                    else:
                        fecha_last_trade = datetime.strptime(
                            fecha_last_trade_string, "%Y-%m-%d"
                        ).date()
                    
                    if g['partner_earning'] != 'NaN':
                        monto_a_pagar=  round(calcula_porcentaje_directo(float(g['partner_earning']),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_a_pagar=0
                    
                    ganancia = Registros_ganancias(
                        client = str(int(g['client'])),
                        fpa = fpa,
                        full_name = g['full_name'],
                        country = g['country'],
                        equity = g['equity'],
                        balance = g['balance'],
                        partner_earning = g['partner_earning'],
                        monto_a_pagar=monto_a_pagar,
                        skilling_earning = g['skilling_earning'],
                        skilling_markup = g['skilling_markup'],
                        skilling_commission = g['skilling_commission'],
                        volumen = g['volumen'],
                        fecha_last_trade = fecha_last_trade,
                        fecha_first_trade = fecha_first_trade,
                        closed_trade_count = g['closed_trade_count'],
                        customer_pnl = g['customer_pnl'],
                        deposito_neto = g['deposito_neto'],
                        deposito = g['deposito'],
                        withdrawals = g['withdrawals'],
                        spreak_direct = spred[1].porcentaje,
                        spreak_indirecto = spred[2].porcentaje,
                        spreak_socio = spred[0].porcentaje
                    )
                    
                    
                    if not existe_ganancia(g['client'],fpa, g['full_name'],g['country'],g['equity'],g['balance'],g['partner_earning'],g['skilling_earning'],g['skilling_markup'],g['skilling_commission'],g['volumen'],fecha_last_trade,fecha_first_trade,g['closed_trade_count'],g['customer_pnl'],g['deposito_neto'],g['deposito'], g['withdrawals'],ganancias):
                        ganancia.save()
                        cuenta = Cuenta.objects.filter(fpa=fpa).first()
                        if g['partner_earning'] != 'NaN':
                            cuenta.monto_total += g['partner_earning']
                            cuenta.monto_a_pagar += round(calcula_porcentaje_directo(float(g['partner_earning']),spred[0].porcentaje,spred[1].porcentaje),2)
                            cuenta.save()
                
                
            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"ErrorMessege": "Document is not format"})
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Salto la exception"})
        print("message Archivo CSV recibido y procesado exitosamente.")
        return JsonResponse(
            {"message": "Archivo CSV recibido y procesado exitosamente."}
        )
    else:
        print("error Se esperaba un archivo CSV en la solicitud POST.")
        return JsonResponse(
            {"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400
        )