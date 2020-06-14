from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from buildpc import getBuild

from homepage.models import *
from django.db.models import Max
from links import getLink
from buildpc import getBuild

def index(request):
    if (request.method == 'GET' and 'amount' in request.GET):
        print('Budget:', request.GET['amount'])
        try:
            build = getBuild(float(request.GET['amount']))
            return results(request, build)
        except ValueError:
            return render(request, 'homepage/index.html')

    return render(request, 'homepage/index.html')

def results(request, build):
    full = {
        'build_info': build
    }
    return render(request, 'homepage/results.html', full)