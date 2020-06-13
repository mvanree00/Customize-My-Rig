from django.shortcuts import render
from django.http import HttpResponse
from buildpc import getBuild

from homepage.models import *
from django.db.models import Max
from links import getLink
from buildpc import getBuild

def index(request):
    if (request.method == 'GET' and 'amount' in request.GET):
        print('Budget:', request.GET['amount'])
        print(getBuild(float(request.GET['amount'])))

    return render(request, 'homepage/index.html')