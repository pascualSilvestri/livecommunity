from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...usuarios.models import Spread,Usuario,Cuenta,BonoAPagar
from ...api.models import Registros_ganancias,Registros_cpa,SpreadIndirecto
import re
import json 
from decimal import Decimal


@csrf_exempt  
def ganancia_get_all(request):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.all()
            cpas = Registros_cpa.objects.all()
            spred = Spread.objects.all()
            data=[]
            for r in ganancias:
                if r.pagado == False:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_operacion,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashe',
                            'client':r.client,
                            
                            'isPago':r.pagado
                        }
                    )
            for c in cpas:
                data.append( 
                        {
                            'creacion':c.fecha_creacion,
                            'monto':c.monto,
                            'monto_spread':c.monto,
                            'tipo_comision':'CPA',
                            'client':c.client,
                            'retiro':0,
                            'isPago':c.pagado
                        }
                    )
            
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})


@csrf_exempt  
def ganancia_only_more_cero(request):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            # cpas = Registros_cpa.objects.all()
            data=[]
            for r in ganancias:
                if r.pagado == False and r.partner_earning != 0:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_operacion,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashe',
                            'client':r.client,
                            
                            'isPago':r.pagado
                        }
                    )
            
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':str(e)})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})


@csrf_exempt  
def ganancia_by_id(request,pk):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            cpas = Registros_cpa.objects.filter(fpa=pk)
            spred = Spread.objects.all()
            data=[]
            for r in ganancias:
                # if r.pagado == False and r.fecha_operacion != None:
                if r.fecha_operacion != None:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_operacion,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':r.symbol,
                            'client':r.client,
                            'isPago':r.pagado
                        }
                    )
            
            for c in cpas:
                data.append( 
                        {
                            'creacion':c.fecha_creacion,
                            'monto':c.monto,
                            'monto_spread':c.monto,
                            'tipo_comision':'CPA',
                            'client':c.client,
                            'retiro':0,
                            'isPago':c.pagado
                        }
                    )
                
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})



@csrf_exempt  
def retiros_totales(request):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.all()
            
            data=[]
            for m in ganancias:
                
                data.append({
                    'fpa':m.fpa,
                    'fecha':m.fecha_operacion,
                })
            
            response = JsonResponse({'data':data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})

@csrf_exempt  
def ganancias_total(request):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.all()
            
            total = 0
            
            for m in ganancias:
                if m.pagado == False:
                    total += m.partner_earning
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})


@csrf_exempt  
def ganancias_total_user(request,pk):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            
            total = 0
            
            for m in ganancias:
                if m.pagado == False:
                    total += m.partner_earning
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})
@csrf_exempt  
def ganancias_total_con_porcentaje(request):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            total = 0
            
            for m in ganancias:
                if m.pagado == False:
                    total += round(calcula_porcentaje_directo(float(m.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})

def ganancias_cpa(request):
    if request.method == 'GET':
        try:
            
            cpas = Registros_cpa.objects.filter()
            
            data = []
            
            for r in cpas:
                data.append( 
                    {
                        'client':r.client,
                        'fpa':r.fpa
                        
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})

def ganancias_cpa_by_id(request,pk):
    if request.method == 'GET':
        try:
            
            cpas = Registros_cpa.objects.filter(fpa=pk)
            
            data = []
            
            for r in cpas:
                data.append( 
                    {
                        'client':r.client,
                        'fpa':r.fpa,
                        'monto':r.monto
                        
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})

@csrf_exempt  
def filtarGananciasCpa(request):
    
    if request.method == "GET":    
        try:
            ganancias = Registros_cpa.objects.all()
            data=[]
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.fecha_creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto,
                        'tipo_comision':'CPA',
                        'id_usuario':r.client,
                        'codigo':r.fpa,
                        'isPago':r.pagado
                    }
                )
            response = JsonResponse({'data':data})
            return response

        except Exception:
            return JsonResponse({'error': str(Exception)})
    else:
        return JsonResponse({'error':'The method is invalid'})

@csrf_exempt  
def filtarGananciasCpaById(request,pk):
    if request.method == "GET":    
        try:
            ganancias = Registros_cpa.objects.filter(fpa=pk)
            data=[]
            for r in ganancias:
                
                data.append( 
                    {
                        'creacion':r.fecha_creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto,
                        'tipo_comision':'CPA',
                        'client':r.client,
                        'codigo':r.fpa,
                        'isPago':r.pagado
                    }
                )
            response = JsonResponse({'data':data})
            return response

        except Exception:
            return JsonResponse({'error': str(Exception)})
    else:
        return JsonResponse({'error':'The method is invalid'})
    
@csrf_exempt  
def filtradoGananciasRevshare(request):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.all()
            
            data = []
            
            for r in ganancias:
                monto_spread= round(calcula_porcentaje_directo(float(r.partner_earning,20,10)),2)
                data.append( 
                    {
                        'creacion':r.fecha_operacion,
                        'monto':r.partner_earning,
                        'monto_spread':monto_spread,
                        'tipo_comision':'Reverash',
                        'client':r.client,
                        'codigo':r.fpa,
                        'isPago':r.pagado
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalido'})


def filtrar_ganancias_by_revshare_By_Id(request,pk):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            spred = Spread.objects.all()
            data = []
            
            for r in ganancias:
                monto_spread= round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                if r.pagado == False and r.fecha_operacion != None:
                    data.append( 
                        {
                            'creacion':r.fecha_operacion,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashare',
                            'client':r.client,
                            'codigo':r.fpa,
                            'isPago':r.pagado
                        }
                    )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})



def filterGananciasFecha(request,desde,hasta):
    
    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    
    try:
        if request.method == 'GET':
            ganancias = Registros_ganancias.objects.filter(Q(fecha_operacion__gte=desde) & Q(fecha_operacion__lte=hasta))
            spred = Spread.objects.all()
            data= []
            for r in ganancias:
                if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                else:
                    monto_spread = r.partner_earning
                data.append( 
                
                    {
                        'creacion':r.fecha_operacion,
                        'monto':r.partner_earning,
                        'monto_spread':monto_spread,
                        'tipo_comision':r.symbol,
                        'client':r.client,
                        
                        'isPago':r.pagado
                    }
                
                )
            
            
            response = JsonResponse({'data':data})
            return response
        
    except ValueError:
        print(ValueError)
        return ValueError

def filterGananciasFechaById(request,pk,desde,hasta):
    
    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.filter(Q(fecha_operacion__gte=desde,fpa=pk) & Q(fecha_operacion__lte=hasta,fpa=pk))
            cpas = Registros_cpa.objects.filter(Q(fecha_creacion__gte=desde,fpa=pk) & Q(fecha_creacion__lte=hasta,fpa=pk))
            spred = Spread.objects.all()
            data=[]
            for r in ganancias:
                # if r.pagado == False and r.fecha_operacion != None:
                if r.fecha_operacion != None:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_operacion,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':r.symbol,
                            'client':r.client,
                            'isPago':r.pagado
                        }
                    )
            
            for c in cpas:
                data.append( 
                        {
                            'creacion':c.fecha_creacion,
                            'monto':c.monto,
                            'monto_spread':c.monto,
                            'tipo_comision':'CPA',
                            'client':c.client,
                            'retiro':0,
                            'isPago':c.pagado
                        }
                    )
                
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})

    



def filter_ganancia_to_date_by_id(request,pk,desde,hasta):
    
    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    spread = Spread.objects.all()
    try:
        if request.method == 'GET':
            cpa = Registros_cpa.objects.filter(Q(fecha_creacion__gte=desde,fpa=pk) & Q(fecha_creacion__lte=hasta,fpa=pk))
            ganancias = Registros_ganancias.objects.filter(Q(fecha_operacion__gte=desde) & Q(fecha_operacion__lte=hasta),fpa=pk,pagado=False)
            spread_indirecto = SpreadIndirecto.objects.filter(Q(fecha_creacion__gte=desde) & Q(fecha_creacion__lte=hasta),fpa=pk,pagado=False)
            cuenta = Cuenta.objects.filter(fpa=pk).first()
            
            data= []
            monto_total = 0
            monto_cpa = 0
            monto_directo = 0
            monto_indirecto = 0
            monto_bono_directo = cuenta.monto_bono_directo
            monto_bono_indirecto = cuenta.monto_bono_indirecto
            level_bono_directo = cuenta.level_bono_directo
            level_bono_indirecto = cuenta.level_bono_indirecto
           
            
            for r in ganancias:
                monto_total += r.partner_earning
                monto_directo += r.monto_a_pagar
            
            for s in spread_indirecto:
                monto_indirecto += s.monto
            
            for c in cpa:
                monto_cpa += c.monto
            
            monto_a_pagar =Decimal(monto_directo) + Decimal(monto_indirecto)
            
            data.append( 
                    {                      
                        'monto_total':monto_total,
                        'monto_directo':monto_directo,
                        'monto_indirecto':round(monto_indirecto,2),
                        'monto_cpa':monto_cpa,
                        'monto_bono_directo':monto_bono_directo,
                        'monto_bono_indirecto':monto_bono_indirecto,
                        'level_bono_directo':level_bono_directo,
                        'level_bono_indirecto':level_bono_indirecto,
                        'monto_a_pagar':round(monto_a_pagar,2)
                    }
                )
            
            # round(monto_a_pagar,2)
            response = JsonResponse({'data':data})
            return response
        
    except ValueError:
        return JsonResponse({'error':str(ValueError)})


def ganancias_all_for_id(request,desde,hasta):
    """
    This function retrieves all the earnings data for a given time period and FPA (Fixed Payment Agreement) ID.
    It returns a JSON response with the data organized by FPA ID, and each FPA ID has a list of earnings data associated with it.
    The earnings data includes information about spread, CPA, bonuses, and reversals.
    """
    if request.method == 'GET':
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
            fpa_list= list(fpa_set)
            for g in fpa_list:

                data_for_id = []
                ganancias_by_id=ganancias.filter(Q(fecha_operacion__gte=desde) & Q(fecha_operacion__lte=hasta),fpa=g,pagado=False).exclude(fecha_operacion=None)
                cpa_by_id = cpas.filter(Q(fecha_creacion__gte=desde) & Q(fecha_creacion__lte=hasta),fpa=g,pagado=False).exclude(fecha_creacion=None)
                bonos_by_id = bonos.filter(Q(date__gte=desde) & Q(date__lte=hasta),fpa=g,pagado=False).exclude(date=None)
                spread_indirecto_dy_id = spread_indirecto.filter(Q(fecha_creacion__gte=desde) & Q(fecha_creacion__lte=hasta),fpa=g,pagado=False).exclude(fecha_creacion=None)
                

                for s in spread_indirecto_dy_id:
                     if s.pagado == False:
                        usuario = usuarios.filter(fpa = s.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = 'Usuario no registrado en back office'
                        
                        data_for_id.append({
                            'id':s.id,
                            'creacion': s.fecha_creacion,
                            'monto_spread': s.monto,
                            'monto': s.monto,
                            'tipo':'spreadIndirecto',
                            'client': None,
                            'isPago': s.pagado,
                            'fpa':s.fpa,
                            'wallet':wallet
                        })



                for b in bonos_by_id:
                    if b.pagado == False:
                        usuario = usuarios.filter(fpa = b.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = 'Usuario no registrado en back office'
                        
                        data_for_id.append({
                            'id':b.id_bono,
                            'creacion': b.date,
                            'monto_spread': b.monto_total,
                            'monto': b.monto_total,
                            'tipo':'bono',
                            'client': None,
                            'isPago': b.pagado,
                            'fpa':b.fpa,
                            'wallet':wallet
                        })
                
                
                
                for c in cpa_by_id:
                    if c.pagado == False:
                        usuario = usuarios.filter(fpa = c.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = 'Usuario no registrado en back office'
                        
                        data_for_id.append({
                            'id':c.id,
                            'creacion': c.fecha_creacion,
                            'monto_spread': c.monto,
                            'monto': c.monto,
                            'tipo':'CPA',
                            'client': c.client,
                            'isPago': c.pagado,
                            'fpa':c.fpa,
                            'wallet':wallet
                        })
                
                for r in ganancias_by_id:    
                    if r.monto_a_pagar > 0:
                    
                       
                        monto_spread = r.monto_a_pagar
                        
                        usuario = usuarios.filter(fpa = r.fpa)
                        if usuario.exists():
                            wallet = usuario.first().wallet.__str__()
                        else:
                            wallet = 'Usuario no registrado en back office'
                        data_for_id.append({
                            'id':r.id,
                            'creacion': r.fecha_operacion,
                            'monto': r.partner_earning,
                            'monto_spread': monto_spread,
                            'tipo':'reverashe',
                            'client': r.client,
                            'isPago': r.pagado,
                            'fpa':r.fpa,
                            'wallet':wallet
                        })
                data.append(data_for_id)
            
            data = [subarray for subarray in data if subarray]

            response = JsonResponse({'data': data})

            return response
        except Exception as e:
            return JsonResponse({'Error': str(e)})
    else:
        return JsonResponse({'Error': 'Método inválido'})


@csrf_exempt  
def ganancia_a_pagar(request):

    if request.method == 'PUT':
        try:
            
            datos = json.loads(request.body)
            ganancias = Registros_ganancias.objects.all()
            cpas = Registros_cpa.objects.all()
            cuentas = Cuenta.objects.all()
            bonos = BonoAPagar.objects.all()
            spreads = SpreadIndirecto.objects.all()
            
            for d in datos.get('body'):
                
                ganancia = ganancias.filter(fpa=d['fpa'],id=d['id'])
                cpa = cpas.filter(fpa=d['fpa'],id=d['id'])
                bono = bonos.filter(fpa=d['fpa'],id_bono=d['id'])
                spread = spreads.filter(fpa=d['fpa'],id=d['id'])
                
                # print(ganancia.first().fpa)
                cuenta = cuentas.filter(fpa=d['fpa'])
                if cuenta.exists():
                    c= cuenta.first()
                    
                if bono.exists() and d['tipo']=='bono':
                    bo = bono.first()
                    bo.pagado = True
                    bo_decimal = Decimal(bo.monto_total)
                    c.monto_a_pagar -= bo_decimal
                    bo.save()
                
                if spread.exists() and d['tipo']=='spreadIndirecto':
                    sp = spread.first()
                    sp.pagado = True
                    c.monto_a_pagar -= Decimal(sp.monto)
                    c.spread_indirecto -= Decimal(sp.monto)
                    if c.spread_indirecto < 0:
                        c.spread_indirecto = 0
                    sp.save()

                if cpa.exists() and d['tipo']=='CPA':
                    cp = cpa.first()
                    cp.pagado = True
                    c_decimal = Decimal(cp.monto)
                    c.monto_cpa -= c_decimal
                    # c.monto_a_pagar -= c_decimal
                    cp.save()
                        
                
                if ganancia.exists() and d['tipo']=='reverashe':
                    g = ganancia.first()
                    g.pagado = True
                    g_monto_decimal = Decimal(g.monto_a_pagar)  # Convierte g.monto_a_pagar a Decimal
                    c.monto_a_pagar -= g_monto_decimal
                    c.monto_total -= Decimal(g.partner_earning)
                    c.spread_directo -= Decimal(g.monto_a_pagar)
                    
                    if c.monto_a_pagar < 0:
                        c.monto_a_pagar = 0
                    g.save()
                c.save()        
                
                
            
            return JsonResponse({"data":datos})
            
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo Incorrecto'})

