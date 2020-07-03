"""
Django Views

References:
- Redirect https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/
- Sessions https://stackoverflow.com/questions/7763115/django-passing-data-between-views, https://docs.djangoproject.com/en/3.0/topics/http/sessions/
"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from homepage.models import *
from django.db.models import Max
from buildpc import getBuild
from django.shortcuts import redirect

def index(request):
    if (request.method == 'GET' and 'amount' in request.GET):
        try:
            budget = float(request.GET['amount'])
            if (budget < 0):
                raise ValueError

            request.session['budget'] = budget
            return redirect('/case')
        except ValueError:
            return render(request, 'homepage/index.html')
    else:
        return render(request, 'homepage/index.html')

def case(request):
    if (request.method == 'GET' and ('solid' in request.GET or 'glass' in request.GET or 'white' in request.GET
                                     or 'black' in request.GET or 'idc' in request.GET)):
        preferences = []
        if ('solid' in request.GET and request.GET['solid'] == 'on'):
            preferences.append('solid')
        if ('glass' in request.GET and request.GET['glass'] == 'on'):
            preferences.append('glass')
        if ('white' in request.GET and request.GET['white'] == 'on'):
            preferences.append('white')
        if ('black' in request.GET and request.GET['black'] == 'on'):
            preferences.append('black')
        if ('idc' in request.GET and request.GET['idc'] == 'on'):
            preferences.append('idc')
        request.session['preferences'] = preferences

        return redirect('/results')
    else:
        return render(request, 'homepage/case.html')

def results(request):
    build = getBuild(request.session['budget'], 'gaming', request.session['preferences'])

    full = {
        'build_info': build
    }

    if full['build_info'] is None:
        return render(request, 'homepage/index.html')

    return render(request, 'homepage/results.html', full)


def info(request):
    return render(request, 'homepage/info.html')


def about(request):
    return render(request, 'homepage/about.html')
