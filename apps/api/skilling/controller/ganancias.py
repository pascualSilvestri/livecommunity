from collections import defaultdict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Case, When, Value, DecimalField, Q, Sum  # Asegúrate de importar Sum
from rest_framework.decorators import api_view
from apps.utils.bonos import bonoDirecto, bonoIndirecto
from ....utils.formulas import calcula_porcentaje_directo, calcular_porcentaje_indirecto
from ....usuarios.models import Usuario
from ...skilling.models import (
    CPA,
    Bono_directo_pagado,
    Bono_indirecto_pagado,
    BonoCpa,
    BonoCpaIndirecto,
    Cpa_directo_pagado,
    Cpa_indirecto_pagado,
    Registros_ganancias,
    Registros_cpa,
    Spread_directo_pagado,
    Spread_indirecto_pagado,
    SpreadIndirecto,
    BonoAPagar,
    Spread,
)
from ....utils.funciones import (
    obtener_comisiones_api_skilling_by_id,
    obtener_comisiones_api_skilling,
    parse_date,
)
from django.db.models.functions import Round
import re
import json
from decimal import Decimal
from ...skilling.serializers import (
    RegistrosGananciasSerializer,
    SpreadIndirectoSerializer,
)
from ....usuarios.serializers import UsuarioSerializer
from datetime import datetime  # {{ edit_1 }}
from django.db import transaction




########################################################################################
##############
##############  Nueva estructura de calculo de ganancias 
##############
########################################################################################
# @csrf_exempt
# def obtener_ganancias_cpa_spread_bonos(request, pk, desde, hasta):
#     """
#     Obtiene las ganancias, comisiones y bonos de un usuario específico en un rango de fechas determinado.

#     Esta función filtra las comisiones directas y de la línea descendente, y calcula los montos
#     de los bonos directos e indirectos.

#     Args:
#         request (HttpRequest): Objeto de la solicitud HTTP.
#         pk (int): ID del usuario para el cual se obtienen las ganancias.
#         desde (str): Fecha de inicio del rango en formato 'YYYY-MM-DD'.
#         hasta (str): Fecha de fin del rango en formato 'YYYY-MM-DD'.

#     Returns:
#         JsonResponse: Un objeto que contiene los montos de spread directo, spread indirecto,
#                       bonos y comisiones.

#     Raises:
#         Exception: Si ocurre algún error durante el proceso.
#     """
#     try:
#         # Llamada a la funcion de la libreria utils para obtener las comisiones de la api de skilling por el id del usuaario
#         comisiones_totales = obtener_comisiones_api_skilling(desde, hasta)
#         usuario_downline = Usuario.objects.filter(up_line=pk, fpa__isnull=False).values(
#             "fpa"
#         )
#         usuarios_list = list(usuario_downline)
#         usuarios_list = [usuario["fpa"] for usuario in usuarios_list]

#         comisiones_directas = [
#             {**comision, "monto_cpa": CPA.objects.first().cpa}  # Agregado monto_cpa
#             for comision in comisiones_totales
#             if comision["codigo"] == "LA508S"
#         ]
#         comision_total = len(comisiones_directas) * int(CPA.objects.first().cpa)

#         comisiones_downline = [
#             {**comision, "monto_cpa": CPA.objects.first().cpa}  # Agregado monto_cpa
#             for comision in comisiones_totales
#             if comision["codigo"] in usuarios_list
#         ]
        
#         # Obtener bono indirecto
#         monto_bono_indirecto, level_bono_indirecto = bonoIndirecto(comisiones_downline,comisiones_directas, BonoCpaIndirecto)

#         # Obtener bono directo
#         monto_bono_directo, level_bono_directo = bonoDirecto(comisiones_directas, BonoCpa)

#         # Obtencion de las ganancias de la base de datos
#         ganancias = Registros_ganancias.objects.filter(fecha_operacion__range=(desde, hasta), fpa=pk)
#         spread_indirecto_registros = SpreadIndirecto.objects.filter(fecha_creacion__range=(desde, hasta),fpa=pk)
#         ganancias_list = list(ganancias.values())
#         spread_indirecto_list = list(spread_indirecto_registros.values())
#         spread_directo = sum(g.monto_a_pagar for g in ganancias)
#         spread_indirecto = sum(s.get('monto') for s in spread_indirecto_list)

#         # Convertir los QuerySets a listas de diccionarios
        
#         return JsonResponse(
#             {
#                 "spread_directo": spread_directo,
#                 "comision_cpa_total": comision_total,
#                 "spread_indirecto": spread_indirecto,
#                 "monto_bono_indirecto": monto_bono_indirecto,
#                 "level_bono_indirecto": level_bono_indirecto,
#                 "monto_bono_directo": monto_bono_directo,
#                 "level_bono_directo": level_bono_directo,
#                 "ganancias": ganancias_list,
#                 "spread_indirecto_list": spread_indirecto_list,
#                 "comisiones_directas": comisiones_directas,
#                 "comisiones_downline": comisiones_downline,
#                 "usuarios_downline": usuarios_list,
#             }
#         )
#     except Exception as e:
#         return JsonResponse({"Error": e.__str__()})


@csrf_exempt
def obtener_ganancias_cpa_spread_bonos(request, pk, desde, hasta):
    """
    Obtiene las ganancias, comisiones y bonos de un usuario específico en un rango de fechas determinado.

    Esta función filtra las comisiones directas y de la línea descendente, y calcula los montos
    de los bonos directos e indirectos.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        pk (int): ID del usuario para el cual se obtienen las ganancias.
        desde (str): Fecha de inicio del rango en formato 'YYYY-MM-DD'.
        hasta (str): Fecha de fin del rango en formato 'YYYY-MM-DD'.

    Returns:
        JsonResponse: Un objeto que contiene los montos de spread directo, spread indirecto,
                      bonos y comisiones.

    Raises:
        Exception: Si ocurre algún error durante el proceso.
    """
    try:
        # Obtener el usuario y su fpa
        usuario = Usuario.objects.get(fpa=pk)
        fpa = usuario.fpa

        # Obtener usuarios downline
        usuarios_downline = Usuario.objects.filter(up_line=fpa, fpa__isnull=False).values_list('fpa', flat=True)

        # Obtener el valor de CPA
        cpa_obj = CPA.objects.first()
        cpa_value = int(cpa_obj.cpa) if cpa_obj else 0

        # Obtener comisiones una sola vez
        comisiones_totales = obtener_comisiones_api_skilling(desde, hasta)

        # Crear un diccionario para acceder rápidamente a comisiones por código
        comisiones_por_codigo = defaultdict(list)
        for com in comisiones_totales:
            comisiones_por_codigo[com['codigo']].append(com)

        # Obtener comisiones directas y actualizar el campo 'comision'
        comisiones_directas = comisiones_por_codigo.get(fpa, [])
        for com in comisiones_directas:
            com['comision'] = cpa_value

        # Obtener comisiones downline y actualizar el campo 'comision'
        comisiones_downline = []
        for downline_fpa in usuarios_downline:
            downline_comisiones = comisiones_por_codigo.get(downline_fpa, [])
            for com in downline_comisiones:
                com['comision'] = cpa_value
            comisiones_downline.extend(downline_comisiones)

        # Calcular la comisión total
        comision_total = len(comisiones_directas) * cpa_value

        # Obtener bonos
        monto_bono_indirecto, level_bono_indirecto = bonoIndirecto(
            comisiones_downline, comisiones_directas, BonoCpaIndirecto
        )
        monto_bono_directo, level_bono_directo = bonoDirecto(
            comisiones_directas, BonoCpa
        )

        # Obtener ganancias y spread indirecto del usuario
        ganancias = Registros_ganancias.objects.filter(
            fecha_operacion__range=(desde, hasta),
            fpa=fpa
        )
        spread_indirecto_registros = SpreadIndirecto.objects.filter(
            fecha_creacion__range=(desde, hasta),
            fpa=fpa
        )

        # Calcular spreads
        spread_directo = ganancias.aggregate(total=Sum('monto_a_pagar'))['total'] or 0
        spread_indirecto = spread_indirecto_registros.aggregate(total=Sum('monto'))['total'] or 0

        # Serializar los datos
        ganancias_list = RegistrosGananciasSerializer(ganancias, many=True).data
        spread_indirecto_list = SpreadIndirectoSerializer(spread_indirecto_registros, many=True).data

        return JsonResponse(
            {
                "spread_directo": spread_directo,
                "comision_cpa_total": comision_total,
                "spread_indirecto": spread_indirecto,
                "monto_bono_indirecto": monto_bono_indirecto,
                "level_bono_indirecto": level_bono_indirecto,
                "monto_bono_directo": monto_bono_directo,
                "level_bono_directo": level_bono_directo,
                "ganancias": ganancias_list,
                "spread_indirecto_list": spread_indirecto_list,
                "comisiones_directas": comisiones_directas,
                "comisiones_downline": comisiones_downline,
                "usuarios_downline": list(usuarios_downline),
            }
        )
    except Exception as e:
        return JsonResponse({"Error": str(e)})

#########################################################################################################################
#
#  Codigo de prueba para obtener los datos de ganancias de todos los usuarios Es lento pero parece que trae todo los datos
#
#########################################################################################################################


# @csrf_exempt
# def obtener_ganancias_cpa_spread_bonos_todos(request, desde, hasta):
#     """
#     Obtiene las ganancias, comisiones y bonos de todos los usuarios en un rango de fechas determinado.

#     Esta función filtra las comisiones directas y de la línea descendente para todos los usuarios
#     con un `fpa` válido y calcula los montos de los bonos directos e indirectos.

#     Args:
#         request (HttpRequest): Objeto de la solicitud HTTP.
#         desde (str): Fecha de inicio del rango en formato 'YYYY-MM-DD'.
#         hasta (str): Fecha de fin del rango en formato 'YYYY-MM-DD'.

#     Returns:
#         JsonResponse: Un objeto que contiene las ganancias, spreads, bonos y comisiones
#                       de todos los usuarios.
#     """
#     try:
#         # Obtener todos los usuarios con un `fpa` válido
#         usuarios = list(Usuario.objects.filter(fpa__isnull=False).values('id', 'fpa'))

#         # Obtener comisiones una sola vez fuera del bucle
#         comisiones_totales = obtener_comisiones_api_skilling(desde, hasta)

#         # Obtener todos los registros de ganancias y spread indirecto en una sola consulta
#         ganancias_todos = Registros_ganancias.objects.filter(fecha_operacion__range=(desde, hasta))
#         spread_indirectos_todos = SpreadIndirecto.objects.filter(fecha_creacion__range=(desde, hasta))

#         # Almacenar los resultados de cada usuario
#         resultados_usuarios = []

#         for usuario in usuarios:
#             pk = usuario['id']
#             fpa = usuario['fpa']

#             # Filtrar los usuarios downline una sola vez
#             usuarios_downline = Usuario.objects.filter(up_line=fpa, fpa__isnull=False).values_list('fpa', flat=True)

#             # Filtrar las comisiones directas e indirectas para el usuario actual
#             comisiones_directas = [com for com in comisiones_totales if com["codigo"] == fpa]
#             comisiones_downline = [com for com in comisiones_totales if com["codigo"] in usuarios_downline]
            
#             comision_total = len(comisiones_directas) * int(CPA.objects.first().cpa)

#             # # Obtener bonos
#             # monto_bono_indirecto, level_bono_indirecto = bonoIndirecto(comisiones_downline, comisiones_directas, BonoCpaIndirecto)
#             # monto_bono_directo, level_bono_directo = bonoDirecto(comisiones_directas, BonoCpa)

#             # Filtrar las ganancias y spreads para el usuario actual
#             ganancias_usuario = ganancias_todos.filter(fpa=fpa)
#             spread_indirecto_usuario = spread_indirectos_todos.filter(fpa=fpa)

#             ganancias_list = list(ganancias_usuario.values())
#             spread_indirecto_list = list(spread_indirecto_usuario.values())
#             spread_directo = sum(g.monto_a_pagar for g in ganancias_usuario)
#             spread_indirecto = sum(s['monto'] for s in spread_indirecto_list)

#             # Almacenar los resultados del usuario actual
#             resultados_usuarios.append({
#                 "fpa": fpa,
#                 "spread_directo": spread_directo,
#                 "comision_cpa_total": comision_total,
#                 "spread_indirecto": spread_indirecto,
#                 # "monto_bono_indirecto": monto_bono_indirecto,
#                 # "level_bono_indirecto": level_bono_indirecto,
#                 # "monto_bono_directo": monto_bono_directo,
#                 # "level_bono_directo": level_bono_directo,
#                 "ganancias": ganancias_list,
#                 "spread_indirecto_list": spread_indirecto_list,
#                 "comisiones_directas": comisiones_directas,
#                 "comisiones_downline": comisiones_downline,
#                 "usuarios_downline": list(usuarios_downline),
#             })

#         return JsonResponse({"resultados": resultados_usuarios})

#     except Exception as e:
#         return JsonResponse({"Error": str(e)})



#########################################################################################################################
#
#  Codigo de prueba para obtener los datos de ganancias de todos los usuarios Es rapido pero no se si trae todo los datos
#
#########################################################################################################################




@csrf_exempt
def obtener_ganancias_cpa_spread_bonos_todos(request, desde, hasta):
    try:
        # Obtener todos los usuarios con un `fpa` válido
        usuarios = Usuario.objects.filter(fpa__isnull=False).values('id', 'fpa', 'up_line')

        # Obtener comisiones una sola vez fuera del bucle
        comisiones_totales = obtener_comisiones_api_skilling(desde, hasta)

        # Obtener todos los registros de ganancias y spread indirecto en una sola consulta
        ganancias_todos = Registros_ganancias.objects.filter(
            fecha_operacion__range=(desde, hasta)
        )
        spread_indirectos_todos = SpreadIndirecto.objects.filter(
            fecha_creacion__range=(desde, hasta)
        )

        # Crear diccionarios para acceso rápido
        ganancias_dict = defaultdict(list)
        for g in ganancias_todos:
            ganancias_dict[g.fpa].append(g)
        spread_indirectos_dict = defaultdict(list)
        for s in spread_indirectos_todos:
            spread_indirectos_dict[s.fpa].append(s)

        # Crear un diccionario para mapear up_line a lista de fpa (usuarios downline)
        up_line_to_fpa = defaultdict(list)
        for usuario in usuarios:
            fpa = usuario['fpa']
            up_line = usuario['up_line']
            if up_line:
                up_line_to_fpa[up_line].append(fpa)

        # Crear un diccionario para acceder rápidamente a comisiones por código
        comisiones_por_codigo = defaultdict(list)
        for com in comisiones_totales:
            comisiones_por_codigo[com['codigo']].append(com)

        # Obtener el valor de CPA
        cpa_obj = CPA.objects.first()
        cpa_value = int(cpa_obj.cpa) if cpa_obj else 0

        # Almacenar los resultados de cada usuario
        resultados_usuarios = []

        for usuario in usuarios:
            fpa = usuario['fpa']

            # Obtener usuarios downline del diccionario
            usuarios_downline = up_line_to_fpa.get(fpa, [])

            # Obtener comisiones directas e indirectas para el usuario actual
            comisiones_directas = comisiones_por_codigo.get(fpa, [])
            comisiones_downline = []
            for downline_fpa in usuarios_downline:
                comisiones_downline.extend(comisiones_por_codigo.get(downline_fpa, []))

            # Actualizar el campo 'comision' en comisiones_directas y comisiones_downline
            for com in comisiones_directas:
                com['comision'] = cpa_value
            for com in comisiones_downline:
                com['comision'] = cpa_value

            # Calcular la comisión total
            comision_total = len(comisiones_directas) * cpa_value

            # Obtener ganancias y spreads del usuario
            ganancias_usuario = ganancias_dict.get(fpa, [])
            spread_indirecto_usuario = spread_indirectos_dict.get(fpa, [])

            spread_directo = sum(g.monto_a_pagar for g in ganancias_usuario)
            spread_indirecto = sum(s.monto for s in spread_indirecto_usuario)

            # Obtener bonos
            monto_bono_indirecto, level_bono_indirecto = bonoIndirecto(
                comisiones_downline, comisiones_directas, BonoCpaIndirecto
            )
            monto_bono_directo, level_bono_directo = bonoDirecto(
                comisiones_directas, BonoCpa
            )

            # Serializar los datos
            ganancias_usuario_data = RegistrosGananciasSerializer(ganancias_usuario, many=True).data
            spread_indirecto_usuario_data = SpreadIndirectoSerializer(spread_indirecto_usuario, many=True).data

            # Almacenar los resultados del usuario actual
            resultados_usuarios.append({
                "fpa": fpa,
                "monto_bono_indirecto": monto_bono_indirecto,
                "level_bono_indirecto": level_bono_indirecto,
                "monto_bono_directo": monto_bono_directo,
                "level_bono_directo": level_bono_directo,
                "spread_directo": spread_directo,
                "comision_cpa_total": comision_total,
                "spread_indirecto": spread_indirecto,
                "ganancias": ganancias_usuario_data,
                "spread_indirecto_list": spread_indirecto_usuario_data,
                "comisiones_directas": comisiones_directas,
                "comisiones_downline": comisiones_downline,
                "usuarios_downline": usuarios_downline
            })

        return JsonResponse({"resultados": resultados_usuarios})

    except Exception as e:
        return JsonResponse({"Error": str(e)})
    



@csrf_exempt
def obtener_ganancias_cpa_spread_bonos_to_payment(request, desde, hasta):
    try:
        # Obtener todos los usuarios con un `fpa` válido
        usuarios = Usuario.objects.filter(fpa__isnull=False).values('id', 'fpa', 'up_line','wallet','first_name','last_name')

        # Obtener comisiones una sola vez fuera del bucle
        comisiones_totales = obtener_comisiones_api_skilling(desde, hasta)

        # Obtener todos los registros de ganancias y spread indirecto en una sola consulta
        ganancias_todos = Registros_ganancias.objects.filter(
            fecha_operacion__range=(desde, hasta)
        )
        spread_indirectos_todos = SpreadIndirecto.objects.filter(
            fecha_creacion__range=(desde, hasta)
        )

        # Crear diccionarios para acceso rápido
        ganancias_dict = defaultdict(list)
        for g in ganancias_todos:
            ganancias_dict[g.fpa].append(g)
        spread_indirectos_dict = defaultdict(list)
        for s in spread_indirectos_todos:
            spread_indirectos_dict[s.fpa].append(s)

        # Crear un diccionario para mapear up_line a lista de fpa (usuarios downline)
        up_line_to_fpa = defaultdict(list)
        for usuario in usuarios:
            fpa = usuario['fpa']
            up_line = usuario['up_line']
            if up_line:
                up_line_to_fpa[up_line].append(fpa)

        # Crear un diccionario para acceder rápidamente a comisiones por código
        comisiones_por_codigo = defaultdict(list)
        for com in comisiones_totales:
            comisiones_por_codigo[com['codigo']].append(com)

        # Obtener el valor de CPA
        cpa_obj = CPA.objects.first()
        cpa_value = int(cpa_obj.cpa) if cpa_obj else 0

        # Almacenar los resultados de cada usuario
        resultados_usuarios = []

        for usuario in usuarios:
            fpa = usuario['fpa']

            # Obtener usuarios downline del diccionario
            usuarios_downline = up_line_to_fpa.get(fpa, [])

            # Obtener comisiones directas e indirectas para el usuario actual
            comisiones_directas = comisiones_por_codigo.get(fpa, [])
            comisiones_downline = []
            for downline_fpa in usuarios_downline:
                comisiones_downline.extend(comisiones_por_codigo.get(downline_fpa, []))

            # Actualizar el campo 'comision' en comisiones_directas y comisiones_downline
            for com in comisiones_directas:
                com['comision'] = cpa_value
            for com in comisiones_downline:
                com['comision'] = cpa_value

            # Calcular la comisión total
            comision_total = len(comisiones_directas) * cpa_value

            # Obtener ganancias y spreads del usuario
            ganancias_usuario = ganancias_dict.get(fpa, [])
            spread_indirecto_usuario = spread_indirectos_dict.get(fpa, [])

            spread_directo = sum(g.monto_a_pagar for g in ganancias_usuario)
            spread_indirecto = sum(s.monto for s in spread_indirecto_usuario)

            # Obtener bonos
            monto_bono_indirecto, level_bono_indirecto = bonoIndirecto(
                comisiones_downline, comisiones_directas, BonoCpaIndirecto
            )
            monto_bono_directo, level_bono_directo = bonoDirecto(
                comisiones_directas, BonoCpa
            )

            # Serializar los datos
            ganancias_usuario_data = RegistrosGananciasSerializer(ganancias_usuario, many=True).data
            spread_indirecto_usuario_data = SpreadIndirectoSerializer(spread_indirecto_usuario, many=True).data

            # Almacenar los resultados del usuario actual
            resultados_usuarios.append({
                "id": usuario['id'],
                "fpa": fpa,
                "first_name": usuario['first_name'],
                "last_name": usuario['last_name'],
                "wallet": usuario['wallet'],
                "monto_bono_indirecto": monto_bono_indirecto,
                "level_bono_indirecto": level_bono_indirecto,
                "monto_bono_directo": monto_bono_directo,
                "level_bono_directo": level_bono_directo,
                "spread_directo": spread_directo,
                "comision_cpa_total": comision_total,
                "spread_indirecto": spread_indirecto,
                "ganancias": ganancias_usuario_data,
                "spread_indirecto_list": spread_indirecto_usuario_data,
                "comisiones_directas": comisiones_directas,
                "comisiones_downline": comisiones_downline,
                "usuarios_downline": usuarios_downline
            })

        return JsonResponse({"resultados": resultados_usuarios})

    except Exception as e:
        return JsonResponse({"Error": str(e)})
    
    

# Función para intentar convertir una fecha con diferentes formatos
def parse_fecha(fecha_str):
    formatos = ["%Y-%m-%d", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]
    for formato in formatos:
        try:
            return datetime.strptime(fecha_str, formato)
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha inválido: {fecha_str}")

@csrf_exempt
def post_registros_ganancias_pagadas(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            
            searchDate = data.get('searchDate')
            elementosPagados = data.get('elementosPagados')
            
            if not searchDate or not elementosPagados:
                return JsonResponse({"Error": "Datos 'searchDate' o 'elementosPagados' faltantes o inválidos."}, status=400)
            
            # Validar y procesar las fechas con el manejador de múltiples formatos
            try:
                desde = parse_fecha(searchDate.get('desde', ''))
                hasta = parse_fecha(searchDate.get('hasta', ''))
            except ValueError as e:
                return JsonResponse({"Error": str(e)}, status=400)

            # Listas para guardar los objetos creados
            comisiones_directas_list = []
            comisiones_downline_list = []
            ganancias_list = []
            spread_indirecto_list = []
            bonos_directo_list = []
            bonos_indirecto_list = []

            with transaction.atomic():
                for registro in elementosPagados:
                    fpa_registro = registro.get('fpa')
                    if not fpa_registro:
                        continue

                    # Procesar comisiones directas
                    comisiones_directas = registro.get('comisiones_directas', [])
                    for comision_directa in comisiones_directas:
                        if not comision_directa.get('commission_id') or not comision_directa.get('comision'):
                            continue
                        
                        # Convertir la fecha de creación con el manejador de múltiples formatos
                        try:
                            fecha_creacion = parse_fecha(comision_directa.get('fecha_creacion', ''))
                        except ValueError:
                            fecha_creacion = datetime.now()  # Usar fecha actual como valor predeterminado

                        comisiones_directas_list.append(Cpa_directo_pagado(
                            monto=comision_directa.get('comision', 0),
                            commission_id=comision_directa.get('commission_id'),
                            client=comision_directa.get('id_usuario', ''),
                            fpa=comision_directa.get('codigo', ''),
                            fecha_desde=desde,
                            fecha_hasta=hasta,
                            tipo_comision=comision_directa.get('tipo_comision', ''),
                            fecha_creacion=fecha_creacion
                        ))

                    # Procesar comisiones downline
                    comisiones_downline = registro.get('comisiones_downline', [])
                    for comision_downline in comisiones_downline:
                        if not comision_downline.get('commission_id') or not comision_downline.get('comision'):
                            continue
                        
                        try:
                            fecha_creacion = parse_fecha(comision_downline.get('fecha_creacion', ''))
                        except ValueError:
                            fecha_creacion = datetime.now()

                        comisiones_downline_list.append(Cpa_indirecto_pagado(
                            monto=comision_downline.get('comision', 0),
                            commission_id=comision_downline.get('commission_id'),
                            client=comision_downline.get('id_usuario', ''),
                            fpa=fpa_registro,
                            fpa_child=comision_downline.get('codigo', ''),
                            fecha_desde=desde,
                            fecha_hasta=hasta,
                            tipo_comision=comision_downline.get('tipo_comision', ''),
                            fecha_creacion=fecha_creacion
                        ))

                    # Procesar ganancias
                    ganancias = registro.get('ganancias', [])
                    for ganancia_elemento in ganancias:
                        if not ganancia_elemento.get('deal_id') or not ganancia_elemento.get('client'):
                            continue

                        try:
                            fecha_operacion = parse_fecha(ganancia_elemento.get('fecha_operacion', ''))
                        except ValueError:
                            fecha_operacion = datetime.now()

                        ganancias_list.append(Spread_directo_pagado(
                            client=ganancia_elemento.get('client', ''),
                            symbol=ganancia_elemento.get('symbol', ''),
                            deal_id=ganancia_elemento.get('deal_id'),
                            fpa=ganancia_elemento.get('fpa', ''),
                            full_name=ganancia_elemento.get('full_name', ''),
                            partner_earning=ganancia_elemento.get('partner_earning', 0),
                            monto_a_pagar=ganancia_elemento.get('monto_a_pagar', 0),
                            fecha_operacion=fecha_operacion,
                            position=ganancia_elemento.get('position', ''),
                            spreak_direct=ganancia_elemento.get('spreak_direct', 0),
                            spreak_indirecto=ganancia_elemento.get('spreak_indirecto', 0),
                            spreak_socio=ganancia_elemento.get('spreak_socio', 0),
                            fecha_desde=desde,
                            fecha_hasta=hasta,
                        ))

                    # Procesar spread indirecto
                    spread_indirecto_list_elements = registro.get('spread_indirecto_list', [])
                    for spread_indirecto_elemento in spread_indirecto_list_elements:
                        if not spread_indirecto_elemento.get('id') or not spread_indirecto_elemento.get('monto'):
                            continue
                        
                        try:
                            fecha_creacion = parse_fecha(spread_indirecto_elemento.get('fecha_creacion', ''))
                        except ValueError:
                            fecha_creacion = datetime.now()

                        spread_indirecto_list.append(Spread_indirecto_pagado(
                            id_spread_indirecto=spread_indirecto_elemento.get('id'),
                            monto=spread_indirecto_elemento.get('monto', 0),
                            fpa_child=spread_indirecto_elemento.get('fpa_child', ''),
                            fpa=spread_indirecto_elemento.get('fpa', ''),
                            fecha_creacion=fecha_creacion,
                            fecha_desde=desde,
                            fecha_hasta=hasta
                        ))

                    # Procesar bonos directo
                    level_bono_directo = registro.get('level_bono_directo')
                    monto_bono_directo = registro.get('monto_bono_directo')
                    if level_bono_directo is not None and monto_bono_directo is not None:
                        bonos_directo_list.append(Bono_directo_pagado(
                            monto=monto_bono_directo,
                            fpa=fpa_registro,
                            nivel=level_bono_directo,
                            fecha_desde=desde,
                            fecha_hasta=hasta
                        ))

                    # Procesar bonos indirecto
                    level_bono_indirecto = registro.get('level_bono_indirecto')
                    monto_bono_indirecto = registro.get('monto_bono_indirecto')
                    if level_bono_indirecto is not None and monto_bono_indirecto is not None:
                        bonos_indirecto_list.append(Bono_indirecto_pagado(
                            monto=monto_bono_indirecto,
                            fpa=fpa_registro,
                            nivel=level_bono_indirecto,
                            fecha_desde=desde,
                            fecha_hasta=hasta
                        ))

                # Guardar los objetos en la base de datos usando bulk_create
                Cpa_directo_pagado.objects.bulk_create(comisiones_directas_list)
                Cpa_indirecto_pagado.objects.bulk_create(comisiones_downline_list)
                Spread_directo_pagado.objects.bulk_create(ganancias_list)
                Spread_indirecto_pagado.objects.bulk_create(spread_indirecto_list)
                Bono_directo_pagado.objects.bulk_create(bonos_directo_list)
                Bono_indirecto_pagado.objects.bulk_create(bonos_indirecto_list)

            return JsonResponse({"data": data})
        else:
            return JsonResponse({"Error": "Método inválido"}, status=405)
    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)
    
# @csrf_exempt
# def post_registros_ganancias_pagadas(request):
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)  # Convertir el cuerpo de la solicitud a un diccionario
#             searchDate = data['searchDate']
#             elementosPagados = data['elementosPagados']
            
#             desde = datetime.strptime(searchDate['desde'], "%Y-%m-%d")
#             hasta = datetime.strptime(searchDate['hasta'], "%Y-%m-%d")
            
            
            
#             for registro in elementosPagados:
#                 fpa_registro = registro['fpa']
                
                
                
#                 comisiones_directas = registro['comisiones_directas']
#                 for comision_directa in comisiones_directas:    
#                     comisiones_directas_pagadas = Cpa_directo_pagado(
#                         monto=comision_directa['comision'],
#                         commission_id=comision_directa['commission_id'],
#                         client=comision_directa['id_usuario'],
#                         fpa=comision_directa['codigo'],
#                         fecha_desde=desde,
#                         fecha_hasta=hasta,
#                         tipo_comision=comision_directa['tipo_comision'],
#                         fecha_creacion=comision_directa['fecha_creacion']
#                     )
#                     print('soy 1',comisiones_directas_pagadas.fecha_creacion)
                
                
#                 comisiones_downline = registro['comisiones_downline']
#                 for comision_downline in comisiones_downline:
#                     comisiones_downline_pagadas= Cpa_indirecto_pagado(
#                         monto=comision_downline['comision'],
#                         commission_id=comision_downline['commission_id'],
#                         client=comision_downline['id_usuario'],
#                         fpa=fpa_registro,
#                         fpa_child=comision_downline['codigo'],
#                         fecha_desde=desde,
#                         fecha_hasta=hasta,
#                         tipo_comision=comision_downline['tipo_comision'],
#                         fecha_creacion=comision_directa['fecha_creacion']
#                     )
                
                
#                 ganancias = registro['ganancias']
#                 for ganancia_elemento in ganancias:
#                     ganancias_pagadas = Spread_directo_pagado(
#                         client = ganancia_elemento['client'],
#                         symbol=ganancia_elemento['symbol'],
#                         deal_id=ganancia_elemento['deal_id'],
#                         fpa=ganancia_elemento['fpa'],
#                         full_name = ganancia_elemento['full_name'],
#                         partner_earning = ganancia_elemento['partner_earning'],
#                         monto_a_pagar= ganancia_elemento['monto_a_pagar'],
#                         fecha_operacion = ganancia_elemento['fecha_operacion'],
#                         position=ganancia_elemento['position'],
#                         spreak_direct = ganancia_elemento['spreak_direct'],
#                         spreak_indirecto = ganancia_elemento['spreak_indirecto'],
#                         spreak_socio = ganancia_elemento['spreak_socio'],
#                         fecha_desde= desde,
#                         fecha_hasta= hasta,
#                     )
                    
#                     # print(ganancias_pagadas.fecha_operacion)
                    
                    
#                 spread_indirecto_list = registro['spread_indirecto_list']
#                 for spread_indirecto_elemento in spread_indirecto_list:
#                     spread_indirecto_pagado = Spread_indirecto_pagado(
#                         id_spread_indirecto = spread_indirecto_elemento['id'],
#                         monto= spread_indirecto_elemento['monto'],
#                         fpa_child= spread_indirecto_elemento['fpa_child'],
#                         fpa= spread_indirecto_elemento['fpa'],
#                         fecha_creacion= spread_indirecto_elemento['fecha_creacion'],
#                         fecha_desde= desde,
#                         fecha_hasta= hasta
#                     )
                

                
#                 level_bono_directo =  registro['level_bono_directo']
#                 monto_bono_directo = registro['monto_bono_directo']
#                 bono_directo_pagado = Bono_directo_pagado(
#                     monto= monto_bono_directo,
#                     fpa= fpa_registro,
#                     nivel= level_bono_directo,
#                     fecha_desde= desde,
#                     fecha_hasta= hasta
#                 )
                
                
#                 level_bono_indirecto = registro['level_bono_indirecto']
#                 monto_bono_indirecto = registro['monto_bono_indirecto']

#                 bono_indirecto_pagado = Bono_indirecto_pagado(
#                     monto= monto_bono_indirecto,
#                     fpa= fpa_registro,
#                     nivel= level_bono_indirecto,
#                     fecha_desde= desde,
#                     fecha_hasta= hasta
#                 )
            
            
#             return JsonResponse({"data": data})
#         else:
#             return JsonResponse({"Error": "Metodo invalido"})
#     except Exception as e:
#         return JsonResponse({"Error": e.__str__()})