from django.shortcuts import render
from django.http import HttpResponse
from .models import CPU
from buildpc import getBuild

from homepage.models import *
from django.db.models import Max
from links import getLink
from buildpc import getBuild

def index(request):
    if (request.method == 'GET' and 'amount' in request.GET):
        print('Budget:', request.GET['amount'])
        getBuild(float(request.GET['amount']))
        return render(request, 'homepage/results.html')


    return render(request, 'homepage/index.html')

def results(request):
    
    data = CPU.objects.all()

    cpu = {
        "cpu_data": data
    }
    return render(request, 'homepage/results.html', cpu)
    
