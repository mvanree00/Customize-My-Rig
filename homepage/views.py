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
from links import *

def index(request):
    if (request.method == 'GET' and 'amount' in request.GET):
        try:
            budget = float(request.GET['amount'])
            if (budget < 550):
                raise ValueError
            elif (budget > 2500):
                budget = 2500

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
    if request.method == 'GET' and 'pc-type' in request.GET:
        request.session['pc_type'] = request.GET['pc-type']
        return redirect('/brand')
    else:
        return render(request, 'homepage/type.html')

def brand(request):
    if (request.method == 'GET' and ('intel' in request.GET or 'nvidia' in request.GET or 'AMD' in request.GET
                                     or 'no_brand' in request.GET)):
        brand_preferences = []
        if ('intel' in request.GET and request.GET['intel'] == 'on'):
            brand_preferences.append('intel')
        if ('nvidia' in request.GET and request.GET['nvidia'] == 'on'):
            brand_preferences.append('nvidia')
        if ('AMD' in request.GET and request.GET['AMD'] == 'on'):
            brand_preferences.append('AMD')
        request.session['brand_preferences'] = brand_preferences

        return redirect('/hardware')
    else:
        return render(request, 'homepage/brand.html')

def hardware(request):
    if (request.method == 'GET' and ('storage_type' in request.GET)):
        try:
            storage_space = float(request.GET['amount'])
            if storage_space < 0.5:
                raise ValueError

            request.session['storage_amount'] = storage_space
            request.session['storage'] = request.GET['storage_type']
            try:
                build = BUILD.objects.filter()[0]
                ID = BUILD.objects.latest('build_ID').build_ID + 1
                path = '/results/' + str(ID)
            except IndexError:
                path = '/results'
                
                    
            return redirect(path)
        except ValueError:
            return redirect('/hardware')
    else:
        return render(request, 'homepage/hardware.html')

def results(request, build_ID=0):
    # for new build
    if(build_ID == 0 or build_ID == BUILD.objects.latest('build_ID').build_ID + 1):
        build = getBuild(request.session['budget'], request.session['pc_type'], request.session['case_preferences'],
                        request.session['brand_preferences'], request.session['storage_amount'],
                        request.session['storage'])
        try:
            build.items()
        except AttributeError as e:
            print(e)
            full = {
                'build_info': build,
                'build_ID': build_ID
            }
            if full['build_info'] is None:
                return redirect('index')
            return render(request, 'homepage/results.html', full)
        # takes the links from the build and saves them into the db
        for part, obj in build.items(): 
            if(part == 'BUILD COST'):
                cost = obj
            if(part == "CPU"):
                Cpu_link= obj.links
            if(part == 'GPU'):
                Gpu_link = obj.links
            if(part == 'MEM'):
                Mem_link = obj.links
            if(part == 'FAN'):
                try:
                    obj.links
                    Fan_link = obj.links
                except AttributeError:
                    Fan_link = obj
            if(part == 'STORAGE'):
                S_link = obj.links
            if(part == 'EXTRA'):
                E_link = obj.links
            if(part == 'PWR'):
                Pwr_link = obj.links
            if(part == 'MOBO'):
                Mobo_link = obj.links
            if(part == 'CASE'):
                Case_link = obj.links
        temp = BUILD.objects.filter()
        if not temp:
            ID = 1
        else:
            ID = build_ID
            if(build_ID == 0):
                ID += 1
        try:
            E_link
            b = BUILD(
                build_ID = ID,
                build_Cost = cost,
                CPU_links = Cpu_link,
                GPU_links = Gpu_link,
                MEM_links = Mem_link,
                STORAGE_links = S_link,
                EXTRA_links = E_link,
                PWR_links = Pwr_link,
                CASE_links = Case_link,
                MOBO_links = Mobo_link,
                FAN_links = Fan_link
            )
        except NameError:
            b = BUILD(
                build_ID = ID,
                build_Cost = cost,
                CPU_links = Cpu_link,
                GPU_links = Gpu_link,
                MEM_links = Mem_link,
                STORAGE_links = S_link,
                PWR_links = Pwr_link,
                CASE_links = Case_link,
                MOBO_links = Mobo_link,
                FAN_links = Fan_link
            )
        numBuilds = BUILD.objects.filter(build_ID = ID).count()
        if numBuilds == 0:
            b.save()
        full = {
            'build_info': build,
            'build_ID': build_ID
        }
        if full['build_info'] is None:
            return redirect('index')
        return render(request, 'homepage/results.html', full)
    # for past builds
    else:
        pastBuild = BUILD.objects.filter(build_ID=build_ID)[0]
        if not pastBuild:
            return redirect('index')
        else:
            # makes a different build based on whether it has Extra_links defined or not
            Fan_links = pastBuild.FAN_links
            try:
                Fan_links = FAN.objects.filter(links=Fan_links)[0]
            except IndexError:
                Fan_links = pastBuild.FAN_links
            if pastBuild.EXTRA_links:
                build = {
                    'CPU': CPU.objects.filter(links=pastBuild.CPU_links)[0],
                    'FAN': Fan_links,
                    'GPU': GPU.objects.filter(links=pastBuild.GPU_links)[0],
                    'MOBO': MOBO.objects.filter(links=pastBuild.MOBO_links)[0],
                    'MEM': MEM.objects.filter(links=pastBuild.MEM_links)[0],
                    'CASE': CASE.objects.filter(links=pastBuild.CASE_links)[0],
                    'PWR': PWR.objects.filter(links=pastBuild.PWR_links)[0],
                    'STORAGE': STORAGE.objects.filter(links=pastBuild.STORAGE_links)[0],
                    'EXTRA': STORAGE.objects.filter(links=pastBuild.EXTRA_links)[0],
                    'BUILD COST': pastBuild.build_Cost
                }
                updatedCost = 0
                for part, obj in build.items():
                    if(part == 'BUILD COST'):
                        continue
                    if(part == 'FAN'):
                        try:
                            obj.links
                            checkPart(obj)
                            Fan_link = obj.links
                        except AttributeError:
                            Fan_link = obj
                            continue
                    checkPart(obj)
                    build[part] = obj
                    if obj.price:
                        updatedCost += obj.price
                
                build["BUILD COST"] = updatedCost
                BUILD.objects.filter(build_ID=build_ID).update(
                    build_Cost = build["BUILD COST"],
                    CPU_links = build["CPU"].links,
                    GPU_links = build["GPU"].links,
                    MEM_links = build["MEM"].links,
                    STORAGE_links = build["STORAGE"].links,
                    EXTRA_links = build["EXTRA"].links,
                    PWR_links = build["PWR"].links,
                    CASE_links = build["CASE"].links,
                    MOBO_links = build["MOBO"].links,
                    FAN_links = Fan_link
                )
            else:
                build = {
                    'CPU': CPU.objects.filter(links=pastBuild.CPU_links)[0],
                    'FAN': Fan_links,
                    'GPU': GPU.objects.filter(links=pastBuild.GPU_links)[0],
                    'MOBO': MOBO.objects.filter(links=pastBuild.MOBO_links)[0],
                    'MEM': MEM.objects.filter(links=pastBuild.MEM_links)[0],
                    'CASE': CASE.objects.filter(links=pastBuild.CASE_links)[0],
                    'PWR': PWR.objects.filter(links=pastBuild.PWR_links)[0],
                    'STORAGE': STORAGE.objects.filter(links=pastBuild.STORAGE_links)[0],
                    'BUILD COST': pastBuild.build_Cost
                }
                
                updatedCost = 0
                for part, obj in build.items():
                    if(part == 'BUILD COST'):
                        continue
                    if(part == 'FAN'):
                        try:
                            obj.links
                            checkPart(obj)
                            Fan_link = obj.links
                        except AttributeError:
                            Fan_link = obj
                            continue
                    checkPart(obj)
                    build[part] = obj
                    if obj.price:
                        updatedCost += obj.price

                build["BUILD COST"] = updatedCost
                BUILD.objects.filter(build_ID=build_ID).update(
                    build_Cost=build["BUILD COST"],
                    CPU_links=build["CPU"].links,
                    GPU_links=build["GPU"].links,
                    MEM_links=build["MEM"].links,
                    STORAGE_links=build["STORAGE"].links,
                    PWR_links=build["PWR"].links,
                    CASE_links=build["CASE"].links,
                    MOBO_links=build["MOBO"].links,
                    FAN_links=Fan_link
                )

            full = {
                'build_info': build,
                'build_ID': pastBuild.build_ID
            }
        return render(request, 'homepage/results.html', full)

    


def info(request):
    return render(request, 'homepage/info.html')


def about(request):
    return render(request, 'homepage/about.html')
