from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ....utils.limpiarTablas import limpiar_datos_fpa, limpiar_registros,limpiar_cpa,limpiar_ganacias
from ....utils.funciones import existe,existe_cpa,existe_ganancia
from ....utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ....utils.bonos import bonoDirecto,bonoIndirecto
from ..models import Relation_fpa_client,Registro_archivo,Registros_cpa,Registros_ganancias,SpreadIndirecto
from apps.api.skilling.models import Cuenta,Spread,BonoCpa,BonoCpaIndirecto,CPA
from apps.usuarios.models import Usuario
from datetime import datetime
import pandas as pd
import os
from decimal import Decimal
from django.db.models import Q


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

                    # Buscar si el client ya existe
                    try:
                        client_obj = Relation_fpa_client.objects.get(client=data["id_client"])
                        # Si el client existe y el fpa es None o 'none', actualizar el fpa
                        if client_obj.fpa is None or client_obj.fpa.lower() == 'none':
                            client_obj.fpa = data["fpa"]
                            client_obj.save()
                        # Si el fpa ya tiene otro valor, posiblemente quieras manejar esta situación también
                    except Relation_fpa_client.DoesNotExist:
                        # El client no existe, por lo que se crea uno nuevo
                        Relation_fpa_client.objects.create(
                            fpa=data["fpa"],
                            client=data["id_client"],
                            full_name=data["full_name"],
                            country=data["country"],
                            fecha_registro=fecha_registro,
                            fecha_creacion=fecha_creacion,
                            fecha_verificacion=fecha_verificacion,
                            status=data["status"],
                        )

                        # Crear cuenta si no existe
                        Cuenta.objects.get_or_create(fpa=data["fpa"])

                    except Exception as e:
                        print(e)

            else:
                return JsonResponse({"error": "Document is not format"}, status=402)

        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Salto la exception"}, status=403)

        return JsonResponse({"message": "Archivo CSV recibido y procesado exitosamente."})

    else:
        return JsonResponse({"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=405)



@csrf_exempt
def upload_registros(request):
    """
    End-point para recibir un archivo CSV y procesar los registros de clientes.
    """
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
                        r.fpa = fpa
                        r.status = data['status']
                        r.fecha_calif = fecha_calif
                        r.posicion_cuenta = data['posicion_cuenta']
                        r.volumen = data['volumen']
                        r.primer_deposito = data["primer_deposito"]
                        r.neto_deposito = data["neto_deposito"]
                        r.numeros_depositos = data["numeros_depositos"]
                        if r.fpa is None and r.fpa == 'none':
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
            return JsonResponse({"error": str(e)},status=400)
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
            spred = Spread.objects.all()
            
            excel_file = request.FILES["csvFileGanancias"]
            file_name = excel_file.name
            file_extension = os.path.splitext(file_name)[1]

            if file_extension != ".csv":
                return JsonResponse({"error": "El documento no tiene el formato correcto"}, status=402)

            file_data = pd.read_csv(excel_file)
            new_data = limpiar_ganacias(file_data)
            
            ganancias_a_crear = []
            spread_indirectos_a_crear = []
            
            # Obtener todas las ganancias existentes de una vez
            ganancias_existentes = Registros_ganancias.objects.all()
            
            for g in new_data:
                if g['partner_earning'] <= 0 or g['partner_earning'] == 'NaN':
                    continue

                fpa_id = fpas.filter(client=int(g['client'])).first()
                if fpa_id:
                    fpa = fpa_id.fpa
                    full_name = fpa_id.full_name
                    usuario = Usuario.objects.filter(fpa=fpa).first()
                else:
                    fpa = None
                    full_name = ''
                    usuario = None

                fecha_first_trade = parse_date(str(g["fecha_operacion"]))
                
                monto_a_pagar = round(calcula_porcentaje_directo(float(g['partner_earning']), spred[0].porcentaje, spred[1].porcentaje), 2)
                
                ganancia = Registros_ganancias(
                    client=str(int(g['client'])),
                    position=str(int(g['position'])),
                    symbol=g['symbol'],
                    fpa=fpa,
                    full_name=full_name,
                    partner_earning=g['partner_earning'],
                    monto_a_pagar=monto_a_pagar,
                    fecha_operacion=fecha_first_trade,
                    deal_id=g['deal_id'],
                    spreak_direct=spred[1].porcentaje,
                    spreak_indirecto=spred[2].porcentaje,
                    spreak_socio=spred[0].porcentaje
                )
                
                if not existe_ganancia(ganancia, ganancias_existentes):
                    ganancias_a_crear.append(ganancia)
                    
                    if usuario and usuario.uplink:
                        monto_indirecto = round(calcular_porcentaje_indirecto(monto_a_pagar, spred[2].porcentaje), 2)
                        if monto_indirecto > 0:
                            spread_indirecto = SpreadIndirecto(
                                monto=Decimal(monto_indirecto),
                                fpa_child=fpa,
                                fpa=usuario.uplink,
                                fecha_creacion=fecha_first_trade
                            )
                            spread_indirectos_a_crear.append(spread_indirecto)

            # Crear registros en lote
            Registros_ganancias.objects.bulk_create(ganancias_a_crear)
            SpreadIndirecto.objects.bulk_create(spread_indirectos_a_crear)

        except Exception as e:
            print(str(e))
            return JsonResponse({"Error": str(e)}, status=502)
        
        return JsonResponse({"message": "Archivo CSV recibido y procesado exitosamente."})
    else:
        return JsonResponse({"error": "Se esperaba un archivo CSV en la solicitud POST."}, status=400)

def parse_date(date_string):
    if date_string == "nan":
        return None
    return datetime.strptime(date_string, "%Y-%m-%d").date()







