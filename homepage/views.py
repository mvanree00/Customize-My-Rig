"""
Django Views

References:
- Redirect https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/
- Sessions https://stackoverflow.com/questions/7763115/django-passing-data-between-views, https://docs.djangoproject.com/en/3.0/topics/http/sessions/

TODO:
- Redirect upon error to a page explaining why
- Properly link new questions to database
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
            if (budget < 550):
                raise ValueError

            request.session['budget'] = budget
            return redirect('/case')
        except ValueError:
            return redirect('index')

    return render(request, 'homepage/index.html')

def case(request):
    if (request.method == 'GET' and ('solid' in request.GET or 'glass' in request.GET or 'white' in request.GET
                                     or 'black' in request.GET or 'idc' in request.GET)):
        case_preferences = []
        if ('solid' in request.GET and request.GET['solid'] == 'on'):
            case_preferences.append('solid')
        if ('glass' in request.GET and request.GET['glass'] == 'on'):
            case_preferences.append('glass')
        if ('white' in request.GET and request.GET['white'] == 'on'):
            case_preferences.append('white')
        if ('black' in request.GET and request.GET['black'] == 'on'):
            case_preferences.append('black')
        if ('idc' in request.GET and request.GET['idc'] == 'on'):
            case_preferences.append('idc')
        request.session['case_preferences'] = case_preferences

        return redirect('/type')
    else:
        return render(request, 'homepage/case.html')

def type(request):
    if (request.method == 'GET' and ('type-gaming' in request.GET or 'type-streaming' in request.GET
                                     or 'type-production' in request.GET)):
        if ('type-gaming' in request.GET and request.GET['type-gaming'] == 'on'):
            request.session['pc_type'] = 'gaming'
        elif ('type-streaming' in request.GET and request.GET['type-streaming'] == 'on'):
            request.session['pc_type'] = 'streaming'
        else:
            request.session['pc_type'] = 'production'

        return redirect('/brand')
    else:
        return render(request, 'homepage/type.html')

def brand(request):
    if (request.method == 'GET' and ('intel' in request.GET or 'nvidia' in request.GET or  'AMD' in request.GET )):
        preferences = []
        return redirect('/hardware')
    else:
        return render(request, 'homepage/brand.html')

def hardware(request):
    if (request.method == 'GET' and ('radio-group' in request.GET)):
        preferences = []
        return redirect('/results')
    else:
        return render(request, 'homepage/hardware.html')

def results(request):
    build = getBuild(request.session['budget'], request.session['pc_type'], request.session['case_preferences'])

    full = {
        'build_info': build
    }

    if full['build_info'] is None:
        return redirect('index')

    return render(request, 'homepage/results.html', full)


def info(request):
    return render(request, 'homepage/info.html')


def about(request):
    return render(request, 'homepage/about.html')
