from collections import defaultdict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Case, When, Value, DecimalField, Q, Sum  # Asegúrate de importar Sum

from apps.utils.bonos import bonoDirecto, bonoIndirecto
from ....utils.formulas import calcula_porcentaje_directo, calcular_porcentaje_indirecto
from ....usuarios.models import Usuario
from ...skilling.models import (
    CPA,
    BonoCpa,
    BonoCpaIndirecto,
    Registros_ganancias,
    Registros_cpa,
    SpreadIndirecto,
    BonoAPagar,
    Spread,
)
from ....utils.funciones import (
    obtener_comisiones_api_skilling_by_id,
    obtener_comisiones_api_skilling,
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


@csrf_exempt
def ganancia_get_all(request):
    if request.method != "GET":
        return JsonResponse({"Error": "Método inválido"}, status=405)

    try:
        spread = Spread.objects.all()
        if not spread.exists():
            return JsonResponse({"Error": "No hay registros de Spread"}, status=404)

        spread_directo = spread[0].porcentaje
        spread_indirecto = spread[1].porcentaje

        ganancias = (
            Registros_ganancias.objects.filter(pagado=False)
            .annotate(
                monto_spread=Case(
                    When(
                        partner_earning__gt=0,
                        then=Round(
                            F("partner_earning")
                            * (1 - spread_directo / 100)
                            * (1 - spread_indirecto / 100),
                            2,
                        ),
                    ),
                    default=F("partner_earning"),
                    output_field=DecimalField(),
                )
            )
            .values(
                "fecha_operacion", "partner_earning", "monto_spread", "client", "pagado"
            )
        )

        cpas = Registros_cpa.objects.values(
            "fecha_creacion", "monto", "client", "pagado"
        )

        data = [
            {
                "creacion": g["fecha_operacion"],
                "monto": g["partner_earning"],
                "monto_spread": g["monto_spread"],
                "tipo_comision": "Reverashe",
                "client": g["client"],
                "isPago": g["pagado"],
            }
            for g in ganancias
        ] + [
            {
                "creacion": c["fecha_creacion"],
                "monto": c["monto"],
                "monto_spread": c["monto"],
                "tipo_comision": "CPA",
                "client": c["client"],
                "retiro": 0,
                "isPago": c["pagado"],
            }
            for c in cpas
        ]

        return JsonResponse({"data": data})

    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)


@csrf_exempt
def ganancia_only_more_cero(request):

    if request.method == "GET":
        try:
            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            # cpas = Registros_cpa.objects.all()
            data = []
            for r in ganancias:
                if r.pagado == False and r.partner_earning != 0:
                    if r.partner_earning != 0:
                        monto_spread = round(
                            calcula_porcentaje_directo(
                                float(r.partner_earning),
                                spred[0].porcentaje,
                                spred[1].porcentaje,
                            ),
                            2,
                        )
                    else:
                        monto_spread = r.partner_earning
                    data.append(
                        {
                            "creacion": r.fecha_operacion,
                            "monto": r.partner_earning,
                            "monto_spread": monto_spread,
                            "tipo_comision": "Reverashe",
                            "client": r.client,
                            "isPago": r.pagado,
                        }
                    )

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


@csrf_exempt
def ganancia_by_id(request, pk):

    if request.method == "GET":
        try:
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            cpas = Registros_cpa.objects.filter(fpa=pk)
            spred = Spread.objects.all()
            data = []
            for r in ganancias:
                # if r.pagado == False and r.fecha_operacion != None:
                if r.fecha_operacion != None:
                    if r.partner_earning != 0:
                        monto_spread = round(
                            calcula_porcentaje_directo(
                                float(r.partner_earning),
                                spred[0].porcentaje,
                                spred[1].porcentaje,
                            ),
                            2,
                        )
                    else:
                        monto_spread = r.partner_earning
                    data.append(
                        {
                            "creacion": r.fecha_operacion,
                            "monto": r.partner_earning,
                            "monto_spread": monto_spread,
                            "tipo_comision": r.symbol,
                            "client": r.client,
                            "isPago": r.pagado,
                        }
                    )

            for c in cpas:
                data.append(
                    {
                        "creacion": c.fecha_creacion,
                        "monto": c.monto,
                        "monto_spread": c.monto,
                        "tipo_comision": "CPA",
                        "client": c.client,
                        "retiro": 0,
                        "isPago": c.pagado,
                    }
                )

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": e.__str__()})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


@csrf_exempt
def retiros_totales(request):

    if request.method == "GET":
        try:
            ganancias = Registros_ganancias.objects.all()

            data = []
            for m in ganancias:

                data.append(
                    {
                        "fpa": m.fpa,
                        "fecha": m.fecha_operacion,
                    }
                )

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": e.__str__()})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


@csrf_exempt
def ganancias_total(request):

    if request.method == "GET":
        try:

            ganancias = Registros_ganancias.objects.all()

            total = 0

            for m in ganancias:
                if m.pagado == False:
                    total += m.partner_earning

            response = JsonResponse({"monto": total})

            return response
        except Exception:
            return JsonResponse({"Error": str(Exception)})
    else:
        return JsonResponse({"data": "El metodo es invalido"})


@csrf_exempt
def ganancias_total_user(request, pk):

    if request.method == "GET":
        try:

            ganancias = Registros_ganancias.objects.filter(fpa=pk)

            total = 0

            for m in ganancias:
                if m.pagado == False:
                    total += m.partner_earning

            response = JsonResponse({"monto": total})

            return response
        except Exception:
            return JsonResponse({"Error": str(Exception)})
    else:
        return JsonResponse({"data": "El metodo es invalido"})


@csrf_exempt
def ganancias_total_con_porcentaje(request):

    if request.method == "GET":
        try:

            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            total = 0

            for m in ganancias:
                if m.pagado == False:
                    total += round(
                        calcula_porcentaje_directo(
                            float(m.partner_earning),
                            spred[0].porcentaje,
                            spred[1].porcentaje,
                        ),
                        2,
                    )

            response = JsonResponse({"monto": total})

            return response
        except Exception:
            return JsonResponse({"Error": str(Exception)})
    else:
        return JsonResponse({"data": "El metodo es invalido"})


def ganancias_cpa(request):
    if request.method == "GET":
        try:

            cpas = Registros_cpa.objects.filter()

            data = []

            for r in cpas:
                data.append({"client": r.client, "fpa": r.fpa})

            return JsonResponse({"data": data})

        except Exception:
            return JsonResponse({"Error": Exception})
    else:
        return JsonResponse({"Error": "Metodo invalido"})


def ganancias_cpa_by_id(request, pk):
    if request.method == "GET":
        try:

            cpas = Registros_cpa.objects.filter(fpa=pk)

            data = []

            for r in cpas:
                data.append({"client": r.client, "fpa": r.fpa, "monto": r.monto})

            return JsonResponse({"data": data})

        except Exception:
            return JsonResponse({"Error": Exception})
    else:
        return JsonResponse({"Error": "Metodo invalido"})


@csrf_exempt
def filtarGananciasCpa(request):

    if request.method == "GET":
        try:
            ganancias = Registros_cpa.objects.all()
            data = []
            for r in ganancias:
                data.append(
                    {
                        "creacion": r.fecha_creacion,
                        "monto": r.monto,
                        "monto_spread": r.monto,
                        "tipo_comision": "CPA",
                        "id_usuario": r.client,
                        "codigo": r.fpa,
                        "isPago": r.pagado,
                    }
                )
            response = JsonResponse({"data": data})
            return response

        except Exception:
            return JsonResponse({"error": str(Exception)})
    else:
        return JsonResponse({"error": "The method is invalid"})


@csrf_exempt
def filtarGananciasCpaById(request, pk):
    if request.method == "GET":
        try:
            ganancias = Registros_cpa.objects.filter(fpa=pk)
            data = []
            for r in ganancias:

                data.append(
                    {
                        "creacion": r.fecha_creacion,
                        "monto": r.monto,
                        "monto_spread": r.monto,
                        "tipo_comision": "CPA",
                        "client": r.client,
                        "codigo": r.fpa,
                        "isPago": r.pagado,
                    }
                )
            response = JsonResponse({"data": data})
            return response

        except Exception:
            return JsonResponse({"error": str(Exception)})
    else:
        return JsonResponse({"error": "The method is invalid"})


@csrf_exempt
def filtradoGananciasRevshare(request):

    if request.method == "GET":
        try:

            ganancias = Registros_ganancias.objects.all()

            data = []

            for r in ganancias:
                monto_spread = round(
                    calcula_porcentaje_directo(float(r.partner_earning, 20, 10)), 2
                )
                data.append(
                    {
                        "creacion": r.fecha_operacion,
                        "monto": r.partner_earning,
                        "monto_spread": monto_spread,
                        "tipo_comision": r.symbol,
                        "client": r.client,
                        "codigo": r.fpa,
                        "isPago": r.pagado,
                    }
                )

            return JsonResponse({"data": data})

        except Exception as e:
            return JsonResponse({"Error": e.__str__()})
    else:
        return JsonResponse({"Error": "Metodo invalido"})


def filtrar_ganancias_by_revshare_By_Id(request, pk):

    if request.method == "GET":
        try:

            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            spred = Spread.objects.all()
            data = []

            for r in ganancias:
                monto_spread = round(
                    calcula_porcentaje_directo(
                        float(r.partner_earning),
                        spred[0].porcentaje,
                        spred[1].porcentaje,
                    ),
                    2,
                )
                if r.pagado == False and r.fecha_operacion != None:
                    data.append(
                        {
                            "creacion": r.fecha_operacion,
                            "monto": r.partner_earning,
                            "monto_spread": monto_spread,
                            "tipo_comision": "Reverashare",
                            "client": r.client,
                            "codigo": r.fpa,
                            "isPago": r.pagado,
                        }
                    )

            return JsonResponse({"data": data})

        except Exception:
            return JsonResponse({"Error": Exception})
    else:
        return JsonResponse({"Error": "Metodo invalido"})


def filterGananciasFecha(request, desde, hasta):
    try:
        spread = Spread.objects.all()
        if not spread.exists():
            return JsonResponse({"error": "No hay registros de Spread"}, status=404)

        spread_directo = Decimal(spread[0].porcentaje) / 100
        spread_indirecto = Decimal(spread[1].porcentaje) / 100

        ganancias = (
            Registros_ganancias.objects.filter(fecha_operacion__range=(desde, hasta))
            .annotate(
                monto_spread=Case(
                    When(
                        partner_earning__gt=0,
                        then=Round(
                            F("partner_earning")
                            * (1 - spread_directo)
                            * (1 - spread_indirecto),
                            2,
                        ),
                    ),
                    default=F("partner_earning"),
                    output_field=DecimalField(),
                )
            )
            .values(
                "fecha_operacion",
                "partner_earning",
                "monto_spread",
                "symbol",
                "client",
                "pagado",
            )
        )

        cpas = Registros_cpa.objects.filter(
            fecha_creacion__range=(desde, hasta)
        ).values("fecha_creacion", "monto", "client", "pagado")

        data = [
            {
                "creacion": g["fecha_operacion"],
                "monto": g["partner_earning"],
                "monto_spread": g["monto_spread"],
                "tipo_comision": g["symbol"],
                "client": g["client"],
                "isPago": g["pagado"],
            }
            for g in ganancias
        ] + [
            {
                "creacion": c["fecha_creacion"],
                "monto": c["monto"],
                "monto_spread": c["monto"],
                "tipo_comision": "CPA",
                "client": c["client"],
                "retiro": 0,
                "isPago": c["pagado"],
            }
            for c in cpas
        ]

        return JsonResponse({"data": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def filterGananciasFechaById(request, pk, desde, hasta):
    if request.method == "GET":
        try:
            spread = Spread.objects.all()
            if not spread.exists():
                return JsonResponse({"error": "No hay registros de Spread"}, status=404)

            spread_directo = Decimal(spread[0].porcentaje) / 100
            spread_indirecto = Decimal(spread[1].porcentaje) / 100

            ganancias = (
                Registros_ganancias.objects.filter(
                    fecha_operacion__range=(desde, hasta),
                    fpa=pk,
                    fecha_operacion__isnull=False,
                )
                .annotate(
                    monto_spread=Case(
                        When(
                            partner_earning__gt=0,
                            then=Round(
                                F("partner_earning")
                                * (1 - spread_directo)
                                * (1 - spread_indirecto),
                                2,
                            ),
                        ),
                        default=F("partner_earning"),
                        output_field=DecimalField(),
                    )
                )
                .values(
                    "fecha_operacion",
                    "partner_earning",
                    "monto_spread",
                    "symbol",
                    "client",
                    "pagado",
                )
            )

            cpas = Registros_cpa.objects.filter(
                fecha_creacion__range=(desde, hasta), fpa=pk
            ).values("fecha_creacion", "monto", "client", "pagado")

            data = [
                {
                    "creacion": g["fecha_operacion"],
                    "monto": g["partner_earning"],
                    "monto_spread": g["monto_spread"],
                    "tipo_comision": g["symbol"],
                    "client": g["client"],
                    "isPago": g["pagado"],
                }
                for g in ganancias
            ] + [
                {
                    "creacion": c["fecha_creacion"],
                    "monto": c["monto"],
                    "monto_spread": c["monto"],
                    "tipo_comision": "CPA",
                    "client": c["client"],
                    "retiro": 0,
                    "isPago": c["pagado"],
                }
                for c in cpas
            ]

            return JsonResponse({"data": data})

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return JsonResponse({"Error": "Metodo invalido"})


def filter_ganancia_to_date_by_id(request, pk, desde, hasta):

    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    spread = Spread.objects.all()
    try:
        if request.method == "GET":
            cpa = Registros_cpa.objects.filter(
                Q(fecha_creacion__gte=desde, fpa=pk)
                & Q(fecha_creacion__lte=hasta, fpa=pk)
            )
            ganancias = Registros_ganancias.objects.filter(
                Q(fecha_operacion__gte=desde) & Q(fecha_operacion__lte=hasta), fpa=pk
            )
            spread_indirecto = SpreadIndirecto.objects.filter(
                Q(fecha_creacion__gte=desde) & Q(fecha_creacion__lte=hasta), fpa=pk
            )
            cuenta = Cuenta.objects.filter(fpa=pk).first()

            data = []
            monto_total = 0
            monto_cpa = 0
            monto_directo = 0
            monto_indirecto = 0

            if cuenta != None:
                monto_bono_directo = cuenta.monto_bono_directo
                monto_bono_indirecto = cuenta.monto_bono_indirecto
                level_bono_directo = cuenta.level_bono_directo
                level_bono_indirecto = cuenta.level_bono_indirecto
            else:
                monto_bono_directo = 0
                monto_bono_indirecto = 0
                level_bono_directo = 0
                level_bono_indirecto = 0

            for r in ganancias:
                monto_total += r.partner_earning
                monto_directo += r.monto_a_pagar

            for s in spread_indirecto:
                monto_indirecto += s.monto

            for c in cpa:
                monto_cpa += c.monto

            monto_a_pagar = Decimal(monto_directo) + Decimal(monto_indirecto)

            data.append(
                {
                    "monto_total": monto_total,
                    "monto_directo": monto_directo,
                    "monto_indirecto": round(monto_indirecto, 2),
                    "monto_cpa": monto_cpa,
                    "monto_bono_directo": monto_bono_directo,
                    "monto_bono_indirecto": monto_bono_indirecto,
                    "level_bono_directo": level_bono_directo,
                    "level_bono_indirecto": level_bono_indirecto,
                    "monto_a_pagar": round(monto_a_pagar, 2),
                }
            )

            # round(monto_a_pagar,2)
            response = JsonResponse({"data": data})
            return response

    except ValueError:
        return JsonResponse({"error": str(ValueError)})


def ganancias_all_for_id(request, desde, hasta):
    """
    This function retrieves all the earnings data for a given time period and FPA (Fixed Payment Agreement) ID.
    It returns a JSON response with the data organized by FPA ID, and each FPA ID has a list of earnings data associated with it.
    The earnings data includes information about spread, CPA, bonuses, and reversals.
    """
    if request.method == "GET":
        try:
            ganancias = Registros_ganancias.objects.all()
            cpas = Registros_cpa.objects.all()
            usuarios = Usuario.objects.all()
            spred = Spread.objects.all()
            bonos = BonoAPagar.objects.all()
            spread_indirecto = SpreadIndirecto.objects.all()

            data = []

            fpas_seen = []  # Para evitar duplicados de fpa
            for f in ganancias:
                fpas_seen.append(f.fpa)

            fpa_set = set(fpas_seen)
            fpa_list = list(fpa_set)
            for g in fpa_list:

                data_for_id = []
                ganancias_by_id = ganancias.filter(
                    Q(fecha_operacion__gte=desde) & Q(fecha_operacion__lte=hasta),
                    fpa=g,
                    pagado=False,
                ).exclude(fecha_operacion=None)
                cpa_by_id = cpas.filter(
                    Q(fecha_creacion__gte=desde) & Q(fecha_creacion__lte=hasta),
                    fpa=g,
                    pagado=False,
                ).exclude(fecha_creacion=None)
                bonos_by_id = bonos.filter(
                    Q(date__gte=desde) & Q(date__lte=hasta), fpa=g, pagado=False
                ).exclude(date=None)
                spread_indirecto_dy_id = spread_indirecto.filter(
                    Q(fecha_creacion__gte=desde) & Q(fecha_creacion__lte=hasta),
                    fpa=g,
                    pagado=False,
                ).exclude(fecha_creacion=None)

                for s in spread_indirecto_dy_id:
                    if s.pagado == False:
                        usuario = usuarios.filter(fpa=s.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = "Usuario no registrado en back office"

                        data_for_id.append(
                            {
                                "id": s.id,
                                "creacion": s.fecha_creacion,
                                "monto_spread": s.monto,
                                "monto": s.monto,
                                "tipo": "spreadIndirecto",
                                "client": None,
                                "isPago": s.pagado,
                                "fpa": s.fpa,
                                "wallet": wallet,
                            }
                        )

                for b in bonos_by_id:
                    if b.pagado == False:
                        usuario = usuarios.filter(fpa=b.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = "Usuario no registrado en back office"

                        data_for_id.append(
                            {
                                "id": b.id_bono,
                                "creacion": b.date,
                                "monto_spread": b.monto_total,
                                "monto": b.monto_total,
                                "tipo": "bono",
                                "client": None,
                                "isPago": b.pagado,
                                "fpa": b.fpa,
                                "wallet": wallet,
                            }
                        )

                for c in cpa_by_id:
                    if c.pagado == False:
                        usuario = usuarios.filter(fpa=c.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = "Usuario no registrado en back office"

                        data_for_id.append(
                            {
                                "id": c.id,
                                "creacion": c.fecha_creacion,
                                "monto_spread": c.monto,
                                "monto": c.monto,
                                "tipo": "CPA",
                                "client": c.client,
                                "isPago": c.pagado,
                                "fpa": c.fpa,
                                "wallet": wallet,
                            }
                        )

                for r in ganancias_by_id:
                    if r.monto_a_pagar > 0:

                        monto_spread = r.monto_a_pagar

                        usuario = usuarios.filter(fpa=r.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = "Usuario no registrado en back office"
                        data_for_id.append(
                            {
                                "id": r.id,
                                "creacion": r.fecha_operacion,
                                "monto": r.partner_earning,
                                "monto_spread": monto_spread,
                                "tipo": "reverashe",
                                "client": r.client,
                                "isPago": r.pagado,
                                "fpa": r.fpa,
                                "wallet": wallet,
                            }
                        )
                data.append(data_for_id)

            data = [subarray for subarray in data if subarray]

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Método inválido"})


@csrf_exempt
def ganancia_a_pagar(request):

    if request.method == "PUT":
        try:

            datos = json.loads(request.body)
            ganancias = Registros_ganancias.objects.all()
            cpas = Registros_cpa.objects.all()
            cuentas = Cuenta.objects.all()
            bonos = BonoAPagar.objects.all()
            spreads = SpreadIndirecto.objects.all()

            for d in datos.get("body"):

                ganancia = ganancias.filter(fpa=d["fpa"], id=d["id"])
                cpa = cpas.filter(fpa=d["fpa"], id=d["id"])
                bono = bonos.filter(fpa=d["fpa"], id_bono=d["id"])
                spread = spreads.filter(fpa=d["fpa"], id=d["id"])

                # print(ganancia.first().fpa)
                cuenta = cuentas.filter(fpa=d["fpa"])
                if cuenta.exists():
                    c = cuenta.first()

                if bono.exists() and d["tipo"] == "bono":
                    bo = bono.first()
                    bo.pagado = True
                    bo_decimal = Decimal(bo.monto_total)
                    c.monto_a_pagar -= bo_decimal
                    bo.save()

                if spread.exists() and d["tipo"] == "spreadIndirecto":
                    sp = spread.first()
                    sp.pagado = True
                    c.monto_a_pagar -= Decimal(sp.monto)
                    c.spread_indirecto -= Decimal(sp.monto)
                    if c.spread_indirecto < 0:
                        c.spread_indirecto = 0
                    sp.save()

                if cpa.exists() and d["tipo"] == "CPA":
                    cp = cpa.first()
                    cp.pagado = True
                    c_decimal = Decimal(cp.monto)
                    c.monto_cpa -= c_decimal
                    # c.monto_a_pagar -= c_decimal
                    cp.save()

                if ganancia.exists() and d["tipo"] == "reverashe":
                    g = ganancia.first()
                    g.pagado = True
                    g_monto_decimal = Decimal(
                        g.monto_a_pagar
                    )  # Convierte g.monto_a_pagar a Decimal
                    c.monto_a_pagar -= g_monto_decimal
                    c.monto_total -= Decimal(g.partner_earning)
                    c.spread_directo -= Decimal(g.monto_a_pagar)

                    if c.monto_a_pagar < 0:
                        c.monto_a_pagar = 0
                    g.save()
                c.save()

            return JsonResponse({"data": datos})

        except Exception as e:
            return JsonResponse({"Error": e.__str__()})
    else:
        return JsonResponse({"Error": "Metodo Incorrecto"})

########################################################################################
##############
##############  Nueva estructura de calculo de ganancias 
##############
########################################################################################
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
        # Llamada a la funcion de la libreria utils para obtener las comisiones de la api de skilling por el id del usuaario
        comisiones_totales = obtener_comisiones_api_skilling(desde, hasta)
        usuario_downline = Usuario.objects.filter(up_line=pk, fpa__isnull=False).values(
            "fpa"
        )
        usuarios_list = list(usuario_downline)
        usuarios_list = [usuario["fpa"] for usuario in usuarios_list]

        comisiones_directas = [
            {**comision, "monto_cpa": CPA.objects.first().cpa}  # Agregado monto_cpa
            for comision in comisiones_totales
            if comision["codigo"] == "LA508S"
        ]
        comision_total = len(comisiones_directas) * int(CPA.objects.first().cpa)

        comisiones_downline = [
            {**comision, "monto_cpa": CPA.objects.first().cpa}  # Agregado monto_cpa
            for comision in comisiones_totales
            if comision["codigo"] in usuarios_list
        ]
        
        # Obtener bono indirecto
        monto_bono_indirecto, level_bono_indirecto = bonoIndirecto(comisiones_downline,comisiones_directas, BonoCpaIndirecto)

        # Obtener bono directo
        monto_bono_directo, level_bono_directo = bonoDirecto(comisiones_directas, BonoCpa)

        # Obtencion de las ganancias de la base de datos
        ganancias = Registros_ganancias.objects.filter(fecha_operacion__range=(desde, hasta), fpa=pk)
        spread_indirecto_registros = SpreadIndirecto.objects.filter(fecha_creacion__range=(desde, hasta),fpa=pk)
        ganancias_list = list(ganancias.values())
        spread_indirecto_list = list(spread_indirecto_registros.values())
        spread_directo = sum(g.monto_a_pagar for g in ganancias)
        spread_indirecto = sum(s.get('monto') for s in spread_indirecto_list)

        # Convertir los QuerySets a listas de diccionarios
        
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
                "usuarios_downline": usuarios_list,
            }
        )
    except Exception as e:
        return JsonResponse({"Error": e.__str__()})



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