from django.shortcuts import render

def Home(request):
    return render(request,'index.html')

def Broker(request):
    return render(request,'broker.html')    

def Presenciales(request):
    return render(request,'presenciales.html')    

def Servicios(request):
    return render(request,'servicios.html')    