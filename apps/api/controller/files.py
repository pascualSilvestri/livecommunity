from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...utils.limpiarTablas import limpiar_datos_fpa, limpiar_registros,limpiar_cpa,limpiar_ganacias
from ...utils.funciones import existe,existe_cpa,existe_ganancia
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...utils.bonos import bonoDirecto,bonoIndirecto
from ..models import Relation_fpa_client,Registro_archivo,Registros_cpa,Registros_ganancias,SpreadIndirecto
from ...usuarios.models import Cuenta,Usuario,Spread,BonoCpa,BonoCpaIndirecto,CPA
from datetime import datetime
import pandas as pd
import os
from decimal import Decimal


def convertir_fecha(fecha_string):
    if str(fecha_string) == "nan":
        return None
    else:
        return datetime.strptime(fecha_string, "%Y-%m-%d").date()

@csrf_exempt
def upload_fpa(request):
    if request.method == "POST" and request.FILES.get("csvFileFpa"):
        try:
            csv_file = request.FILES["csvFileFpa"]
            file_name = csv_file.name
            file_extension = os.path.splitext(file_name)[1]

            if file_extension == ".csv":
                file_data = pd.read_csv(csv_file, encoding="utf-8")
                data_limpia = limpiar_datos_fpa(file_data)

                for data in data_limpia:
                    fecha_registro = convertir_fecha(data["fecha_registro"])
                    fecha_creacion = convertir_fecha(data["fecha_creacion_cuenta"])
                    fecha_verificacion = convertir_fecha(data["verificacion"])

                    # Intenta obtener el registro, si no existe, continúa con el siguiente
                    try:
                        registro = Registro_archivo.objects.get(client=data["id_client"])
                        # Si el registro existe y el fpa es None, actualizarlo
                        if registro.fpa is None or registro.fpa == 'none':
                            registro.fpa = data["fpa"]
                            registro.save()
                    except Exception as e:
                        pass

                    try:
                        # Actualizar o crear nueva relación
                        obj, created = Relation_fpa_client.objects.update_or_create(
                            fpa=data["fpa"],
                            client=data["id_client"],
                            defaults={
                                'full_name': data["full_name"],
                                'country': data["country"],
                                'fecha_registro': fecha_registro,
                                'fecha_creacion': fecha_creacion,
                                'fecha_verificacion': fecha_verificacion,
                                'status': data["status"],
                            }
                        )
                        

                        # Crear cuenta si no existe
                        Cuenta.objects.get_or_create(fpa=data["fpa"])

                    except Exception as e:
                        print(e)

            else:
                return JsonResponse({"error": "Document is not format"}, status=402)

        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Salto la exception"},status=403)

        return JsonResponse({"message": "Archivo CSV recibido y procesado exitosamente."})

    else:
        return JsonResponse({"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=405)


# def upload_fpa(request):
#     if request.method == "POST" and request.FILES.get("csvFileFpa"):
#         try:
#             fpas = Relation_fpa_client.objects.all()
#             csv_file = request.FILES["csvFileFpa"]
#             file_name = csv_file.name  # Obtengon el nombre del archivo
#             file_extension = os.path.splitext(file_name)[
#                 1
#             ]  # obtengo la extencion del archivo

#             if file_extension == ".csv":
#                 file_data = pd.read_csv(
#                     csv_file, encoding="utf-8"
#                 )  # obtengo los datos de larchivo

#                 data_limpia = limpiar_datos_fpa(file_data)
#                 # print(data_limpia)
#                 for data in data_limpia:
#                     # print(type(data['id_client']))
#                     fecha_registro_string = str(data["fecha_registro"])
#                     if fecha_registro_string == "nan":
#                         fecha_registro = None
#                     else:
#                         fecha_registro = datetime.strptime(
#                             fecha_registro_string, "%Y-%m-%d"
#                         ).date()

#                     fecha_creacion_string = str(data["fecha_creacion_cuenta"])
#                     if fecha_creacion_string == "nan":
#                         fecha_creacion = None
#                     else:
#                         fecha_creacion = datetime.strptime(
#                             fecha_creacion_string, "%Y-%m-%d"
#                         ).date()

#                     fecha_verificacion_string = str(data["verificacion"])
#                     if fecha_verificacion_string == "nan":
#                         fecha_verificacion = None
#                     else:
#                         fecha_verificacion = datetime.strptime(
#                             fecha_verificacion_string, "%Y-%m-%d"
#                         ).date()

#                     newData = Relation_fpa_client(
#                         fpa=data["fpa"],
#                         client=data["id_client"],
#                         full_name=data["full_name"],
#                         country=data["country"],
#                         fecha_registro=fecha_registro,
#                         fecha_creacion=fecha_creacion,
#                         fecha_verificacion=fecha_verificacion,
#                         status=data["status"],
#                     )
#                     montos= Cuenta(fpa=data["fpa"])
#                     try:
#                         f = Cuenta.objects.filter(fpa=data["fpa"])
#                         if not f.exists():
#                             montos.save()
#                         fpa = fpas.filter(fpa=data["fpa"], client=data["id_client"])
#                         if not fpa.exists():
#                             newData.save()
                            
#                     except Exception as e:
#                         print(e)

#             else:
#                 print("ErrorMessege Document is not format")
#                 return JsonResponse({"error": "Document is not format"},status=402)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"Error": "Salto la exception"})
#         print("message Archivo CSV recibido y procesado exitosamente.")
#         return JsonResponse(
#             {"message": "Archivo CSV recibido y procesado exitosamente."}
#         )
#     else:
#         print("error Se esperaba un archivo CSV en la solicitud POST.")
#         return JsonResponse(
#             {"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400
#         )
    
################################################Registros####################################################
    

# @csrf_exempt
# def upload_registros(request):
#     if request.method == "POST" and request.FILES.get("csvFileRegistro"):
#         try:
#             excel_file = request.FILES["csvFileRegistro"]
#             file_name = excel_file.name
#             file_extension = os.path.splitext(file_name)[1]

#             if file_extension == ".xlsx":
#                 file_data = pd.read_excel(excel_file, engine='openpyxl')
#                 new_data = limpiar_registros(file_data)

#                 for data in new_data:
#                     # Conversión de fechas
#                     fecha_registro = pd.to_datetime(data["fecha_registro"], errors='coerce', format="%Y-%m-%d").date() if data["fecha_registro"] != "none" else None
#                     fecha_calif = pd.to_datetime(data["fecha_calif"], errors='coerce', format="%Y-%m-%d").date() if data["fecha_calif"] != "none" else None
#                     fecha_primer_deposito = pd.to_datetime(data["fecha_primer_deposito"], errors='coerce', format="%Y-%m-%d").date() if data["fecha_primer_deposito"] != "none" else None

#                     # Obtener o crear el fpa correspondiente
#                     fpa_obj = Relation_fpa_client.objects.filter(client=data['client']).first()
#                     fpa = fpa_obj.fpa if fpa_obj else None

#                     # Actualizar o crear el registro
#                     registro, created = Registro_archivo.objects.update_or_create(
#                         client=data['client'],
#                         fecha_registro=fecha_registro,
#                         country=data['country'],
#                         defaults={
#                             'fpa': fpa,
#                             'status': data['status'],
#                             'fecha_calif': fecha_calif,
#                             'posicion_cuenta': data['posicion_cuenta'],
#                             'volumen': data['volumen'],
#                             'primer_deposito': data['primer_deposito'],
#                             'fecha_primer_deposito': fecha_primer_deposito,
#                             'neto_deposito': data['neto_deposito'],
#                             'numeros_depositos': data['numeros_depositos'],
#                             'comision': data['comision'],
#                         }
#                     )
#             else:
#                 return JsonResponse({"error": "Formato de documento no válido"}, status=400)
#         except Exception as e:
#             return JsonResponse({"Error": str(e)}, status=400)

#         return JsonResponse({"message": "Archivo CSV recibido y procesado exitosamente."})
#     else:
#         return JsonResponse({"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400)


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
                    

                    register = registros.filter(client=data['client'],fecha_registro=fecha_registro,country=data['country'])
                    
                    if register.exists():
                        r = register.first()
                        r.primer_deposito = data["primer_deposito"]
                        r.neto_deposito = data["neto_deposito"]
                        r.numeros_depositos = data["numeros_depositos"]
                        if r.fpa is None or r.fpa == 'none':
                            r.fpa = fpa
                        r.save()
                    else:
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
                        
                        # if not existe(data['client'],fecha_registro,fpa,data['status'],fecha_calif,data['country'],data['posicion_cuenta'],fecha_primer_deposito,data['neto_deposito'],data['numeros_depositos'],registros):
                        registro.save()

                
            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"error": "Document is not format"},status=400)
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
            cpa_value = CPA.objects.filter(id=1).first()
            excel_file = request.FILES["csvFileCpa"]
            file_name = excel_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo

            if file_extension == ".xlsx":
                file_data = pd.read_excel(excel_file,engine='openpyxl')  # obtengo los datos de larchivo
                new_data= limpiar_cpa(file_data)
                
                    
                for cpa in new_data:

                    fecha_creacion_string = str(cpa["fecha_creacion"])
                    if fecha_creacion_string == "none":
                        fecha_creacion = None
                    else:
                        fecha_creacion = datetime.strptime(
                            fecha_creacion_string, "%Y-%m-%d"
                        ).date()

                    cpa_queryset = cpas.filter(client=cpa['client'])
                    
                    if cpa_queryset.exists():
                        pass
                    else:
                        fpa_id = fpas.filter(client=cpa['client']).first()
                        if fpa_id:
                            fpa = fpa_id.fpa
                        else:
                            fpa = None

                        new_cpa = Registros_cpa(
                            fecha_creacion= fecha_creacion,
                            monto_real= cpa['monto'],
                            monto= cpa_value.cpa,
                            cpa= cpa['cpa'],
                            client= cpa['client'],
                            fpa= fpa
                        )
                        
                        
                        # if not existe_cpa(fecha_creacion,cpa['monto'],cpa['client'],cpa['fpa'],cpas):
                        bono_directo = BonoCpa
                        bono_indirecto = BonoCpaIndirecto

                        if fpa != None:
                            cuenta = Cuenta.objects.filter(fpa=fpa).first()
                                
                            if cuenta.fpa != 'none':
                                
                                usuario_up_line = Usuario.objects.filter(fpa=fpa)
                                if usuario_up_line.exists():
                                    up_line_usuario = usuario_up_line.first().uplink
                                    cuenta_up_line = Cuenta.objects.filter(fpa=up_line_usuario)
                                else:
                                    cuenta_up_line = None
                                cuenta.monto_cpa += Decimal(cpa_value.cpa)
                                # cuenta.monto_a_pagar += Decimal(cpa['monto'])
                                cuenta.cpa += 1
                                bonoDirecto(cuenta,bono_directo)
                                bonoIndirecto(cuenta,bono_indirecto)
                                if cuenta_up_line != None:
                                    if cuenta_up_line.exists():
                                        cuenta_up = cuenta_up_line.first()
                                        cuenta_up.cpaIndirecto += 1
                                        bonoIndirecto(cuenta_up,bono_indirecto)
                                        cuenta_up.save()
                                new_cpa.save()
                                cuenta.save()
                                # usuario_up_line[0].save()

            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"error": "Document is not format"},status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({"Error": str(e)},status=402)
        print("message Archivo CSV recibido y procesado exitosamente.")
        return JsonResponse(
            {"message": "Archivo CSV recibido y procesado exitosamente."}
        )
    else:
        print("error Se esperaba un archivo CSV en la solicitud POST.")
        return JsonResponse(
            {"error": "Se esperaba un archivo xlsx en la solicitud POST."}, status=400
        )

@csrf_exempt
def upload_ganancias(request):
    if request.method == "POST" and request.FILES.get("csvFileGanancias"):
        try:
            fpas = Relation_fpa_client.objects.all()
            ganancias = Registros_ganancias.objects.all()
            usuarios = Usuario.objects.all()
            cuentas = Cuenta.objects.all()
            spred = Spread.objects.all()
            
            excel_file = request.FILES["csvFileGanancias"] #Obtengo el archivo
            file_name = excel_file.name  # Obtengo el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo

            if file_extension == ".csv":
                file_data = pd.read_csv(excel_file)  # obtengo los datos del archivo
                new_data= limpiar_ganacias(file_data)
                
                for g in new_data:
                    if g['partner_earning'] > 0:
                        fpa_id = fpas.filter(client=int(g['client']))
                        if fpa_id.exists():
                            fpa = fpa_id[0].fpa
                            full_name = fpa_id[0].full_name
                        else:
                            fpa = None
                            full_name=''
                        
                        fecha_first_trade_string = str(g["fecha_operacion"])
                        if fecha_first_trade_string == "nan":
                            fecha_first_trade = None
                        else:
                            fecha_first_trade = datetime.strptime(
                                fecha_first_trade_string, "%Y-%m-%d"
                            ).date()
                        
                        if g['partner_earning'] != 'NaN':
                            monto_a_pagar=  round(calcula_porcentaje_directo(float(g['partner_earning']),spred[0].porcentaje,spred[1].porcentaje),2)
                        else:
                            monto_a_pagar=0
                        
                        ganancia = Registros_ganancias(
                            client = str(int(g['client'])),
                            position=str(int(g['position'])),
                            symbol=g['symbol'],
                            fpa = fpa,
                            full_name = full_name,
                            partner_earning = g['partner_earning'],
                            monto_a_pagar=monto_a_pagar,
                            fecha_operacion = fecha_first_trade,
                            deal_id=g['deal_id'],
                            spreak_direct = spred[1].porcentaje,
                            spreak_indirecto = spred[2].porcentaje,
                            spreak_socio = spred[0].porcentaje
                        )
                        
                        if not existe_ganancia(ganancia,ganancias):
                            
                            usuario = usuarios.filter(fpa=ganancia.fpa)
                            
                            if usuario.exists():
                                up_line = usuario.first().uplink
                            else:
                                up_line = None
                            
                            cuenta = cuentas.filter(fpa=fpa)
                            cuenta_up_line = cuentas.filter(fpa=up_line)
                            
                            if cuenta.exists and g['partner_earning'] != 'NaN':
                                c = cuenta.first()
                                if (c != None):
                                    c.monto_total += Decimal(ganancia.partner_earning)
                                    c.monto_a_pagar += Decimal(ganancia.monto_a_pagar)
                                    c.spread_directo += Decimal(ganancia.monto_a_pagar)
                                    c.save()
                            
                            if cuenta_up_line.exists():
                                c_up_line = cuenta_up_line.first()
                                c_up_line.monto_a_pagar += Decimal(round(calcular_porcentaje_indirecto(ganancia.monto_a_pagar,spred[2].porcentaje),2))
                                c_up_line.spread_indirecto+= Decimal(round(calcular_porcentaje_indirecto(ganancia.monto_a_pagar,spred[2].porcentaje),2))
                                spread_indirecto=SpreadIndirecto(
                                    monto = Decimal(round(calcular_porcentaje_indirecto(ganancia.monto_a_pagar,spred[2].porcentaje),2)),
                                    fpa_child=fpa,
                                    fpa= c_up_line.fpa,
                                    fecha_creacion= fecha_first_trade
                                )
                                if spread_indirecto.monto > 0:
                                    spread_indirecto.save()
                                    c_up_line.save()

                            ganancia.save() 
                        
                        else:
                            ganancia.fpa = fpa
                            
                            ganancia.save()
                                

            else:
                print("ErrorMessege Document is not format")
                return JsonResponse({"error": "Document is not format"},status=402)
        except Exception as e:
            print(str(e))
            return JsonResponse({"Error": "Salto la exception"},status=502)
        return JsonResponse(
            {"message": "Archivo CSV recibido y procesado exitosamente."}
        )
    else:
        print("error Se esperaba un archivo CSV en la solicitud POST.")
        return JsonResponse(
            {"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400
        )








