"""
PC Building Algorithm

References:
- Django Queries: https://docs.djangoproject.com/en/3.0/ref/models/querysets/

TODO:
- account for PSU power ratings
- adjust weights
- pick fan based upon power needs (more power = more heat)
- brainstorm better methodology for picking RAM
"""

from homepage.models import *
from django.db.models import Max
from django.db.models import Q
from links import checkPart

def getBuild(starting_budget, type_='gaming', case=[], brand_preferences=[], storage_amount=0.5, storage_type='either'):
    try:
        ###########
        # WEIGHTS #
        ###########
        print('PC Type:', type_)
        # weighting pc parts based upon pc type selection
        if type_ == 'streaming': #FIXME: weights
            if starting_budget <= 850:
                cpu_weight = 0.25
                gpu_weight = 0.375
            else:
                cpu_weight = 0.25
                gpu_weight = 0.15
        elif type_ == 'gaming':
            if starting_budget <= 850:
                cpu_weight = 0.25
                gpu_weight = 0.375
            elif starting_budget < 1650:
                cpu_weight = 0.3
                gpu_weight = 0.4
            else:
                cpu_weight = .315
                gpu_weight = .44
        else: #FIXME: weights, production
            if starting_budget <= 850:
                cpu_weight = 0.25
                gpu_weight = 0.375
            else:
                cpu_weight = 0.3
                gpu_weight = 0.2
        parts = {}
        budget_remaining = starting_budget

        ########
        # CASE #
        ########
        while True:
            if 'idc' in case: # no case preference, lowest price case chosen
                case_obj = CASE.objects.filter(price__isnull = False).order_by('price')[0]
            else: # case preferences, spending no more than 10% of budget
                case_objs = CASE.objects.filter(price__isnull = False).filter(price__lte=starting_budget*0.10)\
                    .order_by('price')

                # Narrow by color selections
                if 'white' in case and 'black' in case: # White AND/OR black case
                    case_objs = case_objs.filter(Q(color__contains='White') | Q(color__contains='Black'))
                elif 'white' in case:
                    case_objs = case_objs.filter(color__contains = 'White')
                elif 'black' in case:
                    case_objs = case_objs.filter(color__contains = 'Black')

                # Narrow by solid colors
                if 'solid' in case:
                    case_objs = case_objs.exclude(color__contains='/')

                # Narrow by panel
                if 'glass' in case:
                    case_objs = case_objs.filter(panel = True)

                if case_objs.exists():
                    case_obj = case_objs[0]
                else:
                    case_obj = None

                # If all options cannot be fulfilled, at the bare minimum get the color correct
                if case_obj is None:
                    case_objs = CASE.objects.filter(price__isnull=False).order_by('price')

                    if 'white' in case and 'black' in case:
                        case_objs = case_objs.filter(Q(color__contains='White') | Q(color__contains='Black'))\
                            .filter(price__lte=starting_budget * 0.10)
                    elif 'white' in case:
                        case_objs = case_objs.filter(color__contains='White').filter(price__lte=starting_budget * 0.10)
                    elif 'black' in case:
                        case_objs = case_objs.filter(color__contains='Black').filter(price__lte=starting_budget * 0.10)

                    case_obj = case_objs.order_by('price')[0]
            if checkPart(case_obj):
                break

        budget_remaining -= case_obj.price

        #########################
        # CPU, FAN, MOTHERBOARD #
        #########################
        # finds best CPU Motherboard combo based on overall performance AND performance ratios (performance divided by total cost)
        cpu_brand_attempts = 0
        while True:
            mobo_objs = MOBO.objects.filter(price__isnull=False, price__lte=cpu_weight * starting_budget)

            # filters cpus based on brand preferences (only sees if possible twice)
            if cpu_brand_attempts <= 1:
                print('Brand preferences:',brand_preferences)
                cpu_objs = CPU.objects.none()

                for brand in brand_preferences: # creates query set of ALL CPUs with the preferred brands
                    cpu_objs = cpu_objs.union(CPU.objects.filter(price__isnull=False,
                                                                 name__icontains=brand,
                                                                 price__lte=cpu_weight * starting_budget))

                if cpu_objs:
                    cpu_brand_attempts += 1
                else: # if brand preference is always gonna be empty, no point in doing it again
                    cpu_brand_attempts = 2
            else: # brand preference attempts failed
                cpu_objs = CPU.objects.filter(price__isnull=False, price__lte=cpu_weight * starting_budget)

            best_cpu = None
            best_mobo = None
            best_fan = None
            best_perf_ratio = 0.0
            if cpu_objs and mobo_objs: # if query returned results, find best CPU + MOBO combo
                cpu_best_combined_perf = cpu_objs.order_by('combined_perf').reverse()[0].combined_perf
                cpu_best_gaming_perf = cpu_objs.order_by('gaming_perf').reverse()[0].gaming_perf
                cpu_best_workstation_perf = cpu_objs.order_by('workstation_perf').reverse()[0].workstation_perf
                for cpu in cpu_objs:
                    # considers fan price
                    fan = 'Built-in'
                    fan_price = 0
                    if cpu.cpu_fan == False:
                        fan = FAN.objects.filter(price__isnull = False).order_by('price')[0]
                        fan_price = fan.price
                    for mobo in mobo_objs:
                        if cpu.platform == mobo.chipset:
                            if (type_ == 'streaming' and cpu.combined_perf > cpu_best_combined_perf - 2 and
                                cpu.combined_perf / (cpu.price+mobo.price+fan_price) > best_perf_ratio): # combined perf ratio
                                best_perf_ratio = cpu.combined_perf / (cpu.price+mobo.price+fan_price)
                                best_cpu = cpu
                                best_mobo = mobo
                                best_fan = fan
                                best_fan_price = fan_price
                            elif (type_ == 'gaming' and cpu.gaming_perf > cpu_best_gaming_perf - 2 and
                                cpu.gaming_perf / (cpu.price+mobo.price+fan_price) > best_perf_ratio): # gaming perf ratio
                                best_perf_ratio = cpu.gaming_perf / (cpu.price + mobo.price + fan_price)
                                best_cpu = cpu
                                best_mobo = mobo
                                best_fan = fan
                                best_fan_price = fan_price
                            elif (type_ == 'production' and cpu.workstation_perf > cpu_best_workstation_perf - 2 and
                                cpu.workstation_perf / (cpu.price+mobo.price+fan_price) > best_perf_ratio): # workstation perf ratio
                                best_perf_ratio = cpu.workstation_perf / (cpu.price + mobo.price + fan_price)
                                best_cpu = cpu
                                best_mobo = mobo
                                best_fan = fan
                                best_fan_price = fan_price

            # ensures CPU + MOBO combination creator did not fail before checking parts
            if not(best_cpu is None or best_mobo is None or best_fan is None) and \
                checkPart(best_cpu) and checkPart(best_mobo) and (best_fan == 'Built-in' or checkPart(best_fan)):
                break
        budget_remaining -= best_cpu.price
        budget_remaining -= best_mobo.price
        budget_remaining -= best_fan_price

        #######
        # GPU #
        #######
        # for streaming/gaming PCs, gaming performance benchmark used with performance ratio
        # for production, video memory important so considered here (https://nerdtechy.com/workstation-vs-gaming-pc)
        gpu_brand_attempts = 0
        while True:
            # filters gpus based on brand preferences (attempts finding brand matches maximum of twice)
            gpu_objs = GPU.objects.filter(price__isnull=False, price__lte=gpu_weight * starting_budget)
            if gpu_brand_attempts <= 1:
                for brand in brand_preferences:
                    gpu_objs = gpu_objs.union(GPU.objects.filter(price__isnull = False,
                                                                 manufacturer__icontains=brand,
                                                                 price__lte=gpu_weight * starting_budget))
                if gpu_objs:
                    gpu_brand_attempts += 1
                else:
                    gpu_brand_attempts = 2

            if gpu_objs: # if gpus in price range
                best_gpu_perf = gpu_objs.order_by('gaming_perf').reverse()[0].gaming_perf
                best_gpu = None
                best_gpu_mem = 0
                best_gpu_perf_ratio = 0
                for gpu in gpu_objs:
                    if type_ == 'production' and gpu.mem > best_gpu_mem and gpu.gaming_perf > best_gpu_perf - 10:
                        best_gpu = gpu
                        best_gpu_mem = gpu.mem
                    elif (type_ == 'streaming' or type_ == 'gaming') and gpu.gaming_perf > best_gpu_perf - 5 and gpu.gaming_perf / gpu.price > best_gpu_perf_ratio:
                        best_gpu = gpu
                        best_gpu_perf_ratio = gpu.gaming_perf / gpu.price > best_gpu_perf_ratio
            else:
                best_gpu = GPU.objects.filter(price__isnull = False).order_by('price')[0]

            if checkPart(best_gpu):
                break
        budget_remaining -= best_gpu.price

        ##########
        # MEMORY #
        ##########
        while True:
            if starting_budget >= 1200:
                mem = MEM.objects.filter(price__isnull = False, modules='32 GB').order_by('price')[0]
            elif starting_budget >= 700:
                mem = MEM.objects.filter(price__isnull = False, modules='16 GB').order_by('price')[0]
            else:
                mem = MEM.objects.filter(price__isnull = False, modules=' 8 GB').order_by('price')[0]
            if checkPart(mem):
                break
        budget_remaining -= mem.price

        #########
        # POWER #
        #########
        while True:
            pwr_required = best_cpu.tdp + best_gpu.tdp + 175
            pwr = PWR.objects.filter(price__isnull = False, wattage__gte=pwr_required).order_by('price')[0]
            if checkPart(pwr):
                break
        budget_remaining -= pwr.price

        # Adding CPU, fan, GPU, motherboard, memory, case, and power to parts list
        parts.update({'CPU' : best_cpu, 'FAN' : best_fan, 'GPU' : best_gpu, 'MOBO' : best_mobo, 'MEM' : mem, 'CASE': case_obj, 'PWR' : pwr})

        ###########
        # STORAGE #
        ###########
        # Spending remaining money on storage
        # if budget remaining is lower than cheapest part, they need the part anyways so have to add
        storage_amount *= 1000

        cheapest_storage = STORAGE.objects.filter(price__isnull=False).order_by('price')[0]
        if budget_remaining <= cheapest_storage.price:
            parts.update({'STORAGE' : cheapest_storage})
            budget_remaining -= cheapest_storage.price
        else:
            i = 1
            total_storage = 0
            while STORAGE.objects.filter(price__lte=budget_remaining).exists() and total_storage < storage_amount and i <= 2:
                while True:
                    storage = None
                    if storage_type == 'SSD' or storage_type == 'HDD': # specific type filtered
                        storage = STORAGE.objects.filter(price__lte=budget_remaining,kind=storage_type,
                                                         capacity__gte=storage_amount*.95).order_by('price')
                    else: # no type filtered
                        storage = STORAGE.objects.filter(price__lte=budget_remaining,kind='SSD',
                                                         capacity__gte=storage_amount * .95).order_by('price')

                    if not storage: # if no preferred disk type at price, gets whatever with at least storage needed
                        storage = STORAGE.objects.filter(price__lte=budget_remaining,
                                                         capacity__gte=storage_amount*.95).order_by('price')
                    if storage and checkPart(storage[0]):
                        break
                    elif not storage: # can't find drive at this price and capacity, choose highest capacity of any drive type
                        while True:
                            temp = STORAGE.objects.filter(price__lte=budget_remaining).aggregate(mx=Max('capacity'))
                            storage = STORAGE.objects.filter(price__lte=budget_remaining,
                                                             capacity__gte=temp['mx'] * .95).order_by('price')
                            if storage and checkPart(storage[0]):
                                break
                        break
                if i == 1:
                    parts.update({'STORAGE' : storage[0]})
                    budget_remaining -= storage[0].price
                    total_storage += storage[0].capacity
                else:
                    parts.update({'EXTRA': storage[0]})
                    budget_remaining -= storage[0].price
                i += 1

        parts.update({'BUILD COST' : round(starting_budget-budget_remaining,2)})
        return parts
    except AttributeError as e:  # if there is no part at budget given, won't cause crash due to none being found when part.price
        print(e)
        return None
    except IndexError as e: # if there is no part at budget given, won't cause error due to indexing empty list
        print(e)
        return None
