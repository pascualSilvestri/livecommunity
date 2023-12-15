from django.shortcuts import render

def Home(request):
    return render(request,'index.html')


#PRIMER SPRIG   
def Broker(request):
    return render(request,'inprocess.html')    

def Presenciales(request):
    return render(request,'inprocess.html')    

def Servicios(request):
    return render(request,'inprocess.html')    


# def Broker(request):
#     return render(request,'broker.html')    

# def Presenciales(request):
#     return render(request,'presenciales.html')    

# def Servicios(request):
#     return render(request,'servicios.html')    