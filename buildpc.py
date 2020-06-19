"""
PC Building Algorithm

References:
- Django Queries: https://docs.djangoproject.com/en/3.0/ref/models/querysets/

TODO:
- account for PSU power ratings
- adjust weights? have only tested 'gaming' which appears reasonable
- pick fan based upon power needs (more power = more heat)
- brainstorm better methodology for picking RAM
"""

from homepage.models import *
from django.db.models import Max
from links import getLink

def getBuild(starting_budget, type='gaming', case='default'):
    try:
        # weighting pc parts based upon pc type selection
        if type == 'desktop':
            cpu_weight = 0.3
            gpu_weight = 0.3
        elif type == 'gaming':
            cpu_weight = 0.3
            gpu_weight = 0.4
        else: # workstation
            cpu_weight = 0.3
            gpu_weight = 0.5

        parts = {}
        budget_remaining = starting_budget

        ########
        # CASE #
        ########
        # if no case chosen, assume no preference on look and choose lowest price
        if case == 'default':
            case_obj = CASE.objects.order_by('price')[0]
        else:
            case_obj = CASE.objects.filter(name=case)[0]
        budget_remaining -= case_obj.price

        #########################
        # CPU, FAN, MOTHERBOARD #
        #########################
        # finds best CPU Motherboard combo based on overall performance AND performance ratios (performance divided by total cost)
        cpu_objs = CPU.objects.filter(price__lte=cpu_weight * starting_budget)
        cpu_best_desktop_perf = cpu_objs.order_by('desktop_perf').reverse()[0].desktop_perf
        cpu_best_gaming_perf = cpu_objs.order_by('gaming_perf').reverse()[0].gaming_perf
        cpu_best_workstation_perf = cpu_objs.order_by('workstation_perf').reverse()[0].workstation_perf
        mobo_objs = MOBO.objects.filter(price__lte=cpu_weight * starting_budget)
        best_cpu = None
        best_mobo = None
        best_fan = None
        best_perf_ratio = 0.0
        best_perf = 0
        for cpu in cpu_objs:
            # considers fan price
            fan = 'Built-in'
            fan_price = 0
            if cpu.cpu_fan == False:
                fan = FAN.objects.order_by('price')[0]
                fan_price = fan.price
            for mobo in mobo_objs:
                if cpu.platform == mobo.chipset:
                    if (type == 'desktop' and cpu.desktop_perf > cpu_best_desktop_perf - 2 and
                        cpu.desktop_perf / (cpu.price+mobo.price+fan_price) > best_perf_ratio): # desktop perf ratio
                        best_perf_ratio = cpu.desktop_perf / (cpu.price+mobo.price+fan_price)
                        best_perf = cpu.desktop_perf
                        best_cpu = cpu
                        best_mobo = mobo
                        best_fan = fan
                        best_fan_price = fan_price
                    elif (type == 'gaming' and cpu.gaming_perf > cpu_best_gaming_perf - 2 and
                        cpu.gaming_perf / (cpu.price+mobo.price+fan_price) > best_perf_ratio): # gaming perf ratio
                        best_perf_ratio = cpu.gaming_perf / (cpu.price + mobo.price + fan_price)
                        best_cpu = cpu
                        best_mobo = mobo
                        best_fan = fan
                        best_fan_price = fan_price
                    elif (type == 'workstation' and cpu.workstation_perf > cpu_best_workstation_perf - 2 and
                        cpu.workstation_perf / (cpu.price+mobo.price+fan_price) > best_perf_ratio): # workstation perf ratio
                        best_perf_ratio = cpu.workstation_perf / (cpu.price + mobo.price + fan_price)
                        best_cpu = cpu
                        best_mobo = mobo
                        best_fan = fan
                        best_fan_price = fan_price
        budget_remaining -= best_cpu.price
        budget_remaining -= best_mobo.price
        budget_remaining -= best_fan_price

        #######
        # GPU #
        #######
        # for desktops/gaming PCs, gaming performance benchmark used with performance ratio
        # for workstations, video memory important so considered here (https://nerdtechy.com/workstation-vs-gaming-pc)
        gpu_objs = GPU.objects.filter(price__lte=gpu_weight * starting_budget)
        best_gpu_perf = gpu_objs.order_by('gaming_perf').reverse()[0].gaming_perf
        best_gpu = None
        best_gpu_mem = 0
        best_gpu_perf_ratio = 0
        for gpu in gpu_objs:
            if type == 'workstation' and gpu.mem > best_gpu_mem and gpu.gaming_perf > best_gpu_perf - 10:
                best_gpu = gpu
                best_gpu_mem = gpu.mem
            elif (type == 'desktop' or type == 'gaming') and gpu.gaming_perf > best_gpu_perf - 5 and gpu.gaming_perf / gpu.price > best_gpu_perf_ratio:
                best_gpu = gpu
                best_gpu_perf_ratio = gpu.gaming_perf / gpu.price > best_gpu_perf_ratio
        budget_remaining -= best_gpu.price

        ##########
        # MEMORY #
        ##########
        if starting_budget >= 1200:
            mem = MEM.objects.filter(modules='32 GB').order_by('price')[0]
        elif starting_budget >= 700:
            mem = MEM.objects.filter(modules='16 GB').order_by('price')[0]
        else:
            mem = MEM.objects.filter(modules=' 8 GB').order_by('price')[0]
        budget_remaining -= mem.price

        #########
        # POWER #
        #########
        pwr_required = best_cpu.tdp + best_gpu.tdp + 175
        pwr = PWR.objects.filter(wattage__gte=pwr_required).order_by('price')[0]
        budget_remaining -= pwr.price

        # Adding CPU, fan, GPU, motherboard, memory, case, and power to parts list
        parts.update({'CPU' : best_cpu, 'FAN' : best_fan, 'GPU' : best_gpu, 'MOBO' : best_mobo, 'MEM' : mem, 'CASE': case_obj, 'PWR' : pwr})

        ###########
        # STORAGE #
        ###########
        # Spending remaining money on storage
        # if budget remaining is lower than cheapest part, they need the part anyways so have to add
        cheapest_storage = STORAGE.objects.order_by('price')[0]
        print(budget_remaining)
        if budget_remaining <= cheapest_storage.price:
            parts.update({'STORAGE' : cheapest_storage})
            budget_remaining -= cheapest_storage.price
        else:
            i = 1
            while STORAGE.objects.filter(price__lte=budget_remaining).exists() and i <= 3:
                best_ssd_objs = STORAGE.objects.filter(kind='SSD',price__lte=budget_remaining).order_by('-capacity','price')
                if best_ssd_objs.exists():
                    storage = best_ssd_objs[0]
                else:
                    storage = STORAGE.objects.order_by('capacity','price')[0]
                budget_remaining -= storage.price
                parts.update({('STORAGE' + str(i) + " " + str(storage.capacity) + " GB " + storage.kind) : storage})
                i += 1

        parts.update({'BUILD COST' : round(starting_budget-budget_remaining,2)})
        return parts
    except AttributeError:  # if there is no part at budget given, won't cause crash due to none being found when part.price
        return None
    except IndexError: # if there is no part at budget given, won't cause error due to indexing empty list
        return None

    """
    #links = {} <<<<<<<<<<<<<<<<< NOTE THAT LINKS DOESN'T WORK COMPLETELY WITH NON-UPDATED PRICES >>>>>>>>>>>>>>>>>>
    objects = {}
    budget = starting_budget
    try:
        temp = CPU.objects.filter(price__lte=starting_budget*.2).aggregate(mx = Max('gaming_perf'))
        CPUobj = CPU.objects.filter(price__lte=starting_budget*.2,gaming_perf=temp['mx']).order_by('price')[0]
        if CPUobj.cpu_fan == False:
            FANobj = FAN.objects.filter()[0]
            budget-=FANobj.price
        budget-=CPUobj.price
        temp = GPU.objects.filter(price__lte=starting_budget*.4).aggregate(mx = Max('gaming_perf'))
        GPUobj = GPU.objects.filter(price__lte=starting_budget*.4,gaming_perf=temp['mx']).order_by('price')[0]
        budget-=GPUobj.price
        minPwr = (CPUobj.tdp + GPUobj.tdp + 175)
        PWRobj = PWR.objects.filter(wattage__gte=minPwr).order_by('price')[0]
        budget-=PWRobj.price
        MOBOobj = MOBO.objects.filter(chipset=CPUobj.platform).order_by('price')[0]
        budget-=MOBOobj.price
        CASEobj = CASE.objects.order_by('price')[0]
        budget-=CASEobj.price
        if starting_budget>=1200:
            MEMobj = MEM.objects.filter(modules='32 GB').order_by('price')[0]
        elif starting_budget>=700:
            MEMobj = MEM.objects.filter(modules='16 GB').order_by('price')[0]
        else:
            MEMobj = MEM.objects.filter(modules=' 8 GB').order_by('price')[0]
        budget-=MEMobj.price
        temp = STORAGE.objects.filter(price__lte=budget,kind='SSD').aggregate(mx = Max('capacity'))
        STORAGEobj = STORAGE.objects.filter(price__lte=budget,kind='SSD',capacity__gte=temp['mx']*.95).order_by('price')[0]
        budget-=STORAGEobj.price
        objects.update({'CPU': CPUobj,'GPU':GPUobj,'MOBO':MOBOobj,'MEM':MEMobj,'CASE':CASEobj,'STORAGE':STORAGEobj,'PWR':PWRobj})
        if budget>30: # extra storage (HDD)
            temp = STORAGE.objects.filter(price__lte=budget).aggregate(mx = Max('capacity'))
            EXTRAobj = STORAGE.objects.filter(price__lte=budget,capacity__gte=temp['mx']*.95).order_by('price')[0]
            budget-=EXTRAobj.price
            print(EXTRAobj,EXTRAobj.capacity,EXTRAobj.price)
            #links.update({'EXTRA' : getLink(EXTRAobj.links)})
            objects.update({'EXTRA' :EXTRAobj})
        print(CPUobj,CPUobj.price)
        print(MOBOobj,MOBOobj.price)
        print(MEMobj,MEMobj.price)
        print(STORAGEobj,STORAGEobj.capacity,STORAGEobj.price)
        print(GPUobj,GPUobj.price)
        print(CASEobj,CASEobj.price)
        print(PWRobj,PWRobj.price,PWRobj.wattage)
        #links.update({'CPU': getLink(CPUobj.links),'GPU':getLink(GPUobj.links),'MOBO':getLink(MOBOobj.links),'MEM':getLink(MEMobj.links),'CASE':getLink(CASEobj.links),'STORAGE':getLink(STORAGEobj.links),'PWR':getLink(PWRobj.links)})
        if CPUobj.cpu_fan == False:
            print(FANobj,FANobj.price)
            #links.update({'FAN' : getLink(FANobj.links)})
            objects.update({'FAN' : FANobj})
        print('Total Build:',starting_budget-round(budget,2))
        objects.update({'BUILD COST' : starting_budget-round(budget,2)})
        #print(objects)
        return objects
    except TypeError: # if there is no CPU, motherboard, etc. at budget given, won't cause crash due to None * float
        return None
    except IndexError: # if there is no CPU, motherboard, etc. at budget given, won't cause crash due to indexing error
        return None
    #"""
