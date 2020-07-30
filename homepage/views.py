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
            if (budget < 500):
                raise ValueError
            elif (budget > 3000):
                budget = 3000

            request.session['budget'] = budget
            return redirect('/case')
        except ValueError:
            return redirect('index')

    return render(request, 'homepage/index.html')

def case(request):
    if (request.method == 'GET' and 'case' in request.GET):
        chosen = request.session['case_choices'][int(request.GET['case'][-1])]
        request.session['case'] = chosen

        return redirect('/type')
    else:
        cases = CASE.objects.filter(price__lte=request.session['budget']*0.10).order_by('price')

        if cases.count() < 3:
            cases = CASE.objects.order_by('price')[:3]

        cases_dict = {}
        for i in range(0, cases.count()):
            cases_dict[('case'+str(i))] = cases[i]
        cases_dict['case_num'] = cases.count()

        case_ids = []
        for case in cases:
            case_ids.append(case.links)
        request.session['case_choices'] = case_ids

        return render(request, 'homepage/case.html', cases_dict)

def type(request):
    if request.method == 'GET' and 'pc-type' in request.GET:
        request.session['pc_type'] = request.GET['pc-type']
        return redirect('/brand')
    else:
        return render(request, 'homepage/type.html')

def brand(request):
    if (request.method == 'GET' and ('Intel' in request.GET or 'nvidia' in request.GET or 'AMD' in request.GET
                                     or 'no_brand' in request.GET)):
        brand_preferences = []
        if ('Intel' in request.GET and request.GET['Intel'] == 'on'):
            brand_preferences.append('Intel')
        if ('nvidia' in request.GET and request.GET['nvidia'] == 'on'):
            brand_preferences.append('nvidia')
        if ('AMD' in request.GET and request.GET['AMD'] == 'on'):
            brand_preferences.append('AMD')
        request.session['brand_preferences'] = brand_preferences
        
        if 'overclock' in request.GET and request.GET['overclock'] == 'overclock':
            request.session['overclock'] = True
        else:
            request.session['overclock'] = False

        if 'cooling' in request.GET and request.GET['cooling'] == 'watercool':
            request.session['cooling'] = 'water'
        elif 'cooling' in request.GET and request.GET['cooling'] == 'aircool':
            request.session['cooling'] = 'air'
        else:
            request.session['cooling'] = 'either'

        return redirect('/hardware')
    else:
        return render(request, 'homepage/brand.html')

def hardware(request):
    if (request.method == 'GET' and ('HDD' in request.GET or 'SSD' in request.GET or 'auto' in request.GET)):
        try:
            ssd_space = float(request.GET['ssdamount'])
            hdd_space = float(request.GET['hddamount'])
            if ssd_space < 0.5 or ssd_space > 4:
                raise ValueError
            if hdd_space < 1 or hdd_space > 8:
                raise ValueError

            request.session['ssd_storage_amount'] = ssd_space
            request.session['hdd_storage_amount'] = hdd_space
            storage_type = []
            if 'auto' in request.GET and request.GET['auto'] == 'on':
                storage_type.append('auto')
            else:
                if 'HDD' in request.GET and request.GET['HDD'] == 'on':
                    storage_type.append('HDD')
                if 'SSD' in request.GET and request.GET['SSD'] == 'on':
                    storage_type.append('SSD')
            request.session['storage'] = storage_type
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

def lower_results(request, build_ID=0):
    if request.method == 'GET' and 'back' in request.GET:
        return redirect('/results/'+ str(request.session['original_build']))

    build_ID=BUILD.objects.count() + 1
    build = getBuild(request.session['budget_modified'], request.session['pc_type'], request.session['case'],
                     request.session['brand_preferences'], request.session['ssd_storage_amount'],
                     request.session['hdd_storage_amount'], request.session['storage'],
                     request.session['overclock'],
                     request.session['cooling'])
    try:
        build.items()
    except AttributeError as e:
        print(e)
        full = {
            'build_info': build,
            'build_ID': build_ID
        }
        return render(request, 'homepage/lower_results.html', full)
    # takes the links from the build and saves them into the db
    S_link = None
    E_link = None
    for part, obj in build.items():
        if (part == 'BUILD COST'):
            cost = obj
        if (part == "CPU"):
            Cpu_link = obj.links
        if (part == 'GPU'):
            Gpu_link = obj.links
        if (part == 'MEM'):
            Mem_link = obj.links
        if (part == 'FAN'):
            try:
                obj.links
                Fan_link = obj.links
            except AttributeError:
                Fan_link = obj
        if (part == 'STORAGE'):
            S_link = obj.links
        if (part == 'EXTRA'):
            E_link = obj.links
        if (part == 'PWR'):
            Pwr_link = obj.links
        if (part == 'MOBO'):
            Mobo_link = obj.links
        if (part == 'CASE'):
            Case_link = obj.links
    ID = BUILD.objects.count() + 1
    if S_link is not None and E_link is not None:
        b = BUILD(
            build_ID=ID,
            build_Cost=cost,
            CPU_links=Cpu_link,
            GPU_links=Gpu_link,
            MEM_links=Mem_link,
            STORAGE_links=S_link,
            EXTRA_links=E_link,
            PWR_links=Pwr_link,
            CASE_links=Case_link,
            MOBO_links=Mobo_link,
            FAN_links=Fan_link
        )
    elif S_link is not None:
        b = BUILD(
            build_ID=ID,
            build_Cost=cost,
            CPU_links=Cpu_link,
            GPU_links=Gpu_link,
            MEM_links=Mem_link,
            STORAGE_links=S_link,
            PWR_links=Pwr_link,
            CASE_links=Case_link,
            MOBO_links=Mobo_link,
            FAN_links=Fan_link
        )
    elif E_link is not None:
        b = BUILD(
            build_ID=ID,
            build_Cost=cost,
            CPU_links=Cpu_link,
            GPU_links=Gpu_link,
            MEM_links=Mem_link,
            EXTRA_links=E_link,
            PWR_links=Pwr_link,
            CASE_links=Case_link,
            MOBO_links=Mobo_link,
            FAN_links=Fan_link
        )
    numBuilds = BUILD.objects.filter(build_ID=ID).count()
    if numBuilds == 0:
        b.save()
    else:
        build_ID += 1
        b.save()
    full = {
        'build_info': build,
        'build_ID': build_ID
    }
    return render(request, 'homepage/lower_results.html', full)

def upper_results(request, build_ID=0):
    if request.method == 'GET' and 'back' in request.GET:
        return redirect('/results/'+ str(request.session['original_build']))

    build_ID=BUILD.objects.count() + 1
    build = getBuild(request.session['budget_modified'], request.session['pc_type'], request.session['case'],
                     request.session['brand_preferences'], request.session['ssd_storage_amount'],
                     request.session['hdd_storage_amount'], request.session['storage'],
                     request.session['overclock'],
                     request.session['cooling'])
    try:
        build.items()
    except AttributeError as e:
        print(e)
        full = {
            'build_info': build,
            'build_ID': build_ID
        }
        return render(request, 'homepage/upper_results.html', full)
    # takes the links from the build and saves them into the db
    S_link = None
    E_link = None
    for part, obj in build.items():
        if (part == 'BUILD COST'):
            cost = obj
        if (part == "CPU"):
            Cpu_link = obj.links
        if (part == 'GPU'):
            Gpu_link = obj.links
        if (part == 'MEM'):
            Mem_link = obj.links
        if (part == 'FAN'):
            try:
                obj.links
                Fan_link = obj.links
            except AttributeError:
                Fan_link = obj
        if (part == 'STORAGE'):
            S_link = obj.links
        if (part == 'EXTRA'):
            E_link = obj.links
        if (part == 'PWR'):
            Pwr_link = obj.links
        if (part == 'MOBO'):
            Mobo_link = obj.links
        if (part == 'CASE'):
            Case_link = obj.links
    ID = BUILD.objects.count() + 1
    if S_link is not None and E_link is not None:
        b = BUILD(
            build_ID=ID,
            build_Cost=cost,
            CPU_links=Cpu_link,
            GPU_links=Gpu_link,
            MEM_links=Mem_link,
            STORAGE_links=S_link,
            EXTRA_links=E_link,
            PWR_links=Pwr_link,
            CASE_links=Case_link,
            MOBO_links=Mobo_link,
            FAN_links=Fan_link
        )
    elif S_link is not None:
        b = BUILD(
            build_ID=ID,
            build_Cost=cost,
            CPU_links=Cpu_link,
            GPU_links=Gpu_link,
            MEM_links=Mem_link,
            STORAGE_links=S_link,
            PWR_links=Pwr_link,
            CASE_links=Case_link,
            MOBO_links=Mobo_link,
            FAN_links=Fan_link
        )
    elif E_link is not None:
        b = BUILD(
            build_ID=ID,
            build_Cost=cost,
            CPU_links=Cpu_link,
            GPU_links=Gpu_link,
            MEM_links=Mem_link,
            EXTRA_links=E_link,
            PWR_links=Pwr_link,
            CASE_links=Case_link,
            MOBO_links=Mobo_link,
            FAN_links=Fan_link
        )
    numBuilds = BUILD.objects.filter(build_ID=ID).count()
    if numBuilds == 0:
        b.save()
    else:
        build_ID += 1
        b.save()
    full = {
        'build_info': build,
        'build_ID': build_ID
    }
    return render(request, 'homepage/upper_results.html', full)

def results(request, build_ID=0):
    if request.method == 'GET' and 'lower' in request.GET:
        request.session['budget_modified'] = request.session['budget'] - request.session['budget'] * 0.10
        if request.session['budget_modified'] < 500.0:
            request.session['budget_modified'] = 500.0
        return redirect('/lower_results')
    elif request.method == 'GET' and 'higher' in request.GET:
        request.session['budget_modified'] = request.session['budget'] + request.session['budget'] * 0.10
        if request.session['budget_modified'] > 3000.0:
            request.session['budget_modified'] = 3000.0
        return redirect('/upper_results')

    # for new build
    if (build_ID == 0 or build_ID == BUILD.objects.latest('build_ID').build_ID + 1):
        build = getBuild(request.session['budget'], request.session['pc_type'], request.session['case'],
                         request.session['brand_preferences'], request.session['ssd_storage_amount'],
                         request.session['hdd_storage_amount'], request.session['storage'],
                         request.session['overclock'],
                         request.session['cooling'])
        try:
            build.items()
        except AttributeError as e:
            print(e)
            full = {
                'build_info': build,
                'build_ID': build_ID
            }
            request.session['original_build'] = build_ID
            return render(request, 'homepage/results.html', full)
        # takes the links from the build and saves them into the db
        S_link = None
        E_link = None
        for part, obj in build.items():
            if (part == 'BUILD COST'):
                cost = obj
            if (part == "CPU"):
                Cpu_link = obj.links
            if (part == 'GPU'):
                Gpu_link = obj.links
            if (part == 'MEM'):
                Mem_link = obj.links
            if (part == 'FAN'):
                try:
                    obj.links
                    Fan_link = obj.links
                except AttributeError:
                    Fan_link = obj
            if (part == 'STORAGE'):
                S_link = obj.links
            if (part == 'EXTRA'):
                E_link = obj.links
            if (part == 'PWR'):
                Pwr_link = obj.links
            if (part == 'MOBO'):
                Mobo_link = obj.links
            if (part == 'CASE'):
                Case_link = obj.links
        temp = BUILD.objects.filter()
        if not temp:
            ID = 1
        else:
            ID = build_ID
            if (build_ID == 0):
                ID += 1
        if S_link is not None and E_link is not None:
            b = BUILD(
                build_ID=ID,
                build_Cost=cost,
                CPU_links=Cpu_link,
                GPU_links=Gpu_link,
                MEM_links=Mem_link,
                STORAGE_links=S_link,
                EXTRA_links=E_link,
                PWR_links=Pwr_link,
                CASE_links=Case_link,
                MOBO_links=Mobo_link,
                FAN_links=Fan_link
            )
        elif S_link is not None:
            b = BUILD(
                build_ID=ID,
                build_Cost=cost,
                CPU_links=Cpu_link,
                GPU_links=Gpu_link,
                MEM_links=Mem_link,
                STORAGE_links=S_link,
                PWR_links=Pwr_link,
                CASE_links=Case_link,
                MOBO_links=Mobo_link,
                FAN_links=Fan_link
            )
        elif E_link is not None:
            b = BUILD(
                build_ID=ID,
                build_Cost=cost,
                CPU_links=Cpu_link,
                GPU_links=Gpu_link,
                MEM_links=Mem_link,
                EXTRA_links=E_link,
                PWR_links=Pwr_link,
                CASE_links=Case_link,
                MOBO_links=Mobo_link,
                FAN_links=Fan_link
            )

        numBuilds = BUILD.objects.filter(build_ID=ID).count()
        if numBuilds == 0:
            b.save()
        full = {
            'build_info': build,
            'build_ID': build_ID
        }
        request.session['original_build'] = build_ID
        return render(request, 'homepage/results.html', full)
    # for past builds
    else:
        try:
            pastBuild = BUILD.objects.filter(build_ID=build_ID)[0]
        except IndexError as e:
            print(e)
            return redirect('index')
        pastBuild = BUILD.objects.filter(build_ID=build_ID)[0]
        # makes a different build based on whether it has Extra_links defined or not
        Fan_links = pastBuild.FAN_links
        try:
            Fan_links = FAN.objects.filter(links=Fan_links)[0]
        except IndexError:
            Fan_links = pastBuild.FAN_links
        if pastBuild.STORAGE_links and pastBuild.EXTRA_links:
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
                if (part == 'BUILD COST'):
                    continue
                if (part == 'FAN'):
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
                EXTRA_links=build["EXTRA"].links,
                PWR_links=build["PWR"].links,
                CASE_links=build["CASE"].links,
                MOBO_links=build["MOBO"].links,
                FAN_links=Fan_link
            )
        elif pastBuild.EXTRA_links:
            build = {
                'CPU': CPU.objects.filter(links=pastBuild.CPU_links)[0],
                'FAN': Fan_links,
                'GPU': GPU.objects.filter(links=pastBuild.GPU_links)[0],
                'MOBO': MOBO.objects.filter(links=pastBuild.MOBO_links)[0],
                'MEM': MEM.objects.filter(links=pastBuild.MEM_links)[0],
                'CASE': CASE.objects.filter(links=pastBuild.CASE_links)[0],
                'PWR': PWR.objects.filter(links=pastBuild.PWR_links)[0],
                'EXTRA': STORAGE.objects.filter(links=pastBuild.EXTRA_links)[0],
                'BUILD COST': pastBuild.build_Cost
            }
            updatedCost = 0
            for part, obj in build.items():
                if (part == 'BUILD COST'):
                    continue
                if (part == 'FAN'):
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
                EXTRA_links=build["EXTRA"].links,
                PWR_links=build["PWR"].links,
                CASE_links=build["CASE"].links,
                MOBO_links=build["MOBO"].links,
                FAN_links=Fan_link
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
                if (part == 'BUILD COST'):
                    continue
                if (part == 'FAN'):
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
        request.session['original_build'] = build_ID
        return render(request, 'homepage/results.html', full)

def info(request):
    return render(request, 'homepage/info.html')


def about(request):
    return render(request, 'homepage/about.html')
