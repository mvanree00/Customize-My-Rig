from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import CPU


def index(request):
    return render(request, 'homepage/index.html')

def results(request):
    
    data = CPU.objects.all()

    cpu = {
        "cpu_data": data
    }
    return render(request, 'homepage/results.html', cpu)
