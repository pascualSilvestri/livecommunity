from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...utils.limpiarTablas import limpiar_datos_fpa, limpiar_registros,limpiar_cpa,limpiar_ganacias
from ...utils.funciones import existe
from ..models import Relation_fpa_client,Registro_archivo
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
                    try:
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

            print(file_extension)


            if file_extension == ".xlsx":
                file_data = pd.read_excel(excel_file)  # obtengo los datos de larchivo
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
            # fpas = Relation_fpa_client.objects.all()
            # registros=Registro_archivo.objects.all()
            excel_file = request.FILES["csvFileCpa"]
            file_name = excel_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo

            print(file_extension)


            if file_extension == ".xlsx":
                file_data = pd.read_excel(excel_file)  # obtengo los datos de larchivo
                new_data= limpiar_cpa(file_data)
                print(new_data)
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
            # fpas = Relation_fpa_client.objects.all()
            # registros=Registro_archivo.objects.all()
            excel_file = request.FILES["csvFileGanancias"]
            file_name = excel_file.name  # Obtengon el nombre del archivo
            file_extension = os.path.splitext(file_name)[1]  # obtengo la extencion del archivo

            print(file_extension)


            if file_extension == ".csv":
                file_data = pd.read_csv(excel_file)  # obtengo los datos de larchivo
                new_data= limpiar_ganacias(file_data)
                print(new_data)
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
