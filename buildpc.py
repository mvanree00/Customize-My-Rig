"""
PC Building Algorithm

References:
- Django Queries: https://docs.djangoproject.com/en/3.0/ref/models/querysets/

TODO:
- pick fan based upon power needs (more power = more heat)
- m.2 vs sata SSD selections
"""

from homepage.models import *
from django.db.models import Max
from django.db.models import Q
from links import checkPart,checkMem

def getBuild(starting_budget, type_='gaming', case='any', brand_preferences=[], storage_amount=0.5, hdd_storage_amount=1.0,
             storage_type=[], overclock=False, cooling='either'):
    try:
        print('=======PREFERENCE INFO=======')
        print('PC Type:',type_)
        print('Storage Choice:',storage_type)
        print('Storage Amounts (SSD and HDD):',storage_amount,hdd_storage_amount)
        print('Overclocking:', overclock)
        print('Cooling Choice:', cooling)
        ###########
        # WEIGHTS #
        ###########
        print('PC Type:', type_)
        # weighting pc parts based upon pc type selection
        if type_ == 'streaming':
            if starting_budget <= 850:
                cpu_weight = .45
            elif starting_budget < 1650:
                cpu_weight = 0.4
            else:
                cpu_weight = .35
        elif type_ == 'gaming':
            if starting_budget <= 850:
                cpu_weight = 0.375
            elif starting_budget < 1650:
                cpu_weight = 0.35
            else:
                cpu_weight = .325
        else:
            if starting_budget < 1650:
                cpu_weight = 0.6
            else:
                cpu_weight = .66
        parts = {}
        budget_remaining = starting_budget
        ###########
        # STORAGE #
        ###########
        # Meet the desired storage preferences, if not specified give 500gb ssd
        storage_amount *= 1000
        hdd_storage_amount *= 1000
        best_ssd = None
        best_hdd = None
        for types in storage_type:
            if types=='SSD':
                while True:
                    storage = STORAGE.objects.filter(price__lte=budget_remaining,kind=types, price__isnull = False,
                                                    capacity__gte=storage_amount*.95).order_by('price')
                    storage2 = STORAGE.objects.filter(price__lte=budget_remaining,form='M.2 (M)', price__isnull = False,
                                                    capacity__gte=storage_amount*.95).order_by('price')
                    if storage2 and storage and storage[0].price*1.1 < storage2[0].price:
                        if storage and checkPart(storage[0]):
                            best_ssd=storage[0]
                            budget_remaining -= storage[0].price
                            break
                    elif not storage2:
                        if storage and checkPart(storage[0]):
                            best_ssd=storage[0]
                            budget_remaining -= storage[0].price
                            break
                    elif storage and storage[0].capacity*.95<=storage2[0].capacity:
                        if storage2 and checkPart(storage2[0]):
                            best_ssd=storage2[0]
                            budget_remaining -= storage2[0].price
                            break
            elif types=='HDD':
                while True:
                    storage = STORAGE.objects.filter(price__lte=budget_remaining, price__isnull = False,
                                                    capacity__gte=hdd_storage_amount*.95).order_by('price').exclude(kind='SSD')
                    if storage and checkPart(storage[0]):
                        best_hdd = storage[0]
                        budget_remaining -= storage[0].price
                        break
            elif types == 'auto' and len(storage_type) == 1:
                while True:
                    storage = STORAGE.objects.filter(price__lte=budget_remaining,kind='SSD',price__isnull = False,
                                                    capacity__gte=500*.95).order_by('price')
                    if storage and checkPart(storage[0]):
                        best_ssd = storage[0]
                        budget_remaining -= storage[0].price
                        break
        ########
        # CASE #
        ########
        while True:
            case_obj = CASE.objects.filter(links=case)[0]
            if checkPart(case_obj):
                break

        budget_remaining -= case_obj.price

        ##########
        # MEMORY #
        ##########
        while True:
            if starting_budget >= 1200:
                mem = MEM.objects.filter(price__isnull = False, modules='32 GB', realspeed__isnull = False).order_by('-speedperdollar','price')[0]
            elif starting_budget >= 700:
                mem = MEM.objects.filter(price__isnull = False, modules='16 GB', realspeed__isnull = False).order_by('-speedperdollar','price')[0]
            else:
                mem = MEM.objects.filter(price__isnull = False, modules=' 8 GB', realspeed__isnull = False).order_by('-speedperdollar','price')[0]
            if checkMem(mem):
                break
        budget_remaining -= mem.price

        #########
        # POWER #
        #########
        estimated_wattage = 0
        actual_wattage = 0
        while True:
            if type_=='gaming' or type_=='streaming':
                estimated_wattage=525
            else:
                estimated_wattage=450
            if overclock:
                    estimated_wattage += 75
            pwr_objs = PWR.objects.filter(price__isnull = False, wattage__gte=estimated_wattage).order_by('price')

            # base power supply
            pwr = pwr_objs[0]
            price_cap = pwr.price * 0.10 + pwr.price

            # Titanium
            pwr_titanium = pwr_objs.filter(rating='80+ Titanium',
                                    price__lte=price_cap).order_by('price')
            if pwr_titanium:
                pwr = pwr_titanium[0]
            else:
                # Platinum
                pwr_platinum = pwr_objs.filter(rating='80+ Platinum',
                                            price__lte=price_cap).order_by('price')
                if pwr_platinum:
                    pwr = pwr_platinum[0]
                else:
                    # Gold
                    pwr_gold = pwr_objs.filter(rating='80+ Gold',
                                                price__lte=price_cap).order_by('price')
                    if pwr_gold:
                        pwr = pwr_gold[0]
                    else:
                        # Silver
                        pwr_silver = pwr_objs.filter(rating='80+ Silver',
                                                price__lte=price_cap).order_by('price')
                        if pwr_silver:
                            pwr = pwr_silver[0]
                        else:
                            # Bronze
                            pwr_bronze = pwr_objs.filter(rating='80+ Bronze',
                                                        price__lte=price_cap).order_by('price')
                            if pwr_bronze:
                                pwr = pwr_bronze[0]
            if checkPart(pwr):
                break
        mainBudget=budget_remaining-pwr.price
        #########################
        # CPU, FAN, MOTHERBOARD #
        #########################
        # finds best CPU Motherboard combo based on overall performance AND performance ratios (performance divided by total cost)
        while True:
            cpu_brands= []
            for brand in brand_preferences:
                if brand == 'Intel':
                    cpu_brands.append('Intel')
                elif brand == 'AMD':
                    cpu_brands.append('AMD')
            if len(cpu_brands) == 1:
                if cpu_brands[0] == 'Intel':
                    mobo_objs = MOBO.objects.filter(price__isnull=False, chipset__startswith='LGA', price__lte=cpu_weight * mainBudget)
                else:
                    mobo_objs = MOBO.objects.filter(price__isnull=False, price__lte=cpu_weight * mainBudget).exclude(chipset__startswith='LGA')
            else:
                mobo_objs = MOBO.objects.filter(price__isnull=False, price__lte=cpu_weight * mainBudget)

            # filters cpus based on brand preferences (only sees if possible twice)
            print('Brand preferences:',brand_preferences)
            cpu_objs = CPU.objects.none()
            for brand in brand_preferences: # creates query set of ALL CPUs with the preferred brands
                    cpu_objs = cpu_objs.union(CPU.objects.filter(price__isnull=False,
                                                                name__startswith=brand,
                                                                price__lte=cpu_weight * mainBudget))
            if not cpu_objs: # brand preference attempts failed
                cpu_objs = CPU.objects.filter(price__isnull=False, price__lte=cpu_weight * mainBudget)
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
                    temp_mobo = mobo_objs.filter(chipset=cpu.platform)
                    if temp_mobo:
                        for mobo in temp_mobo:
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
                                    
                if best_cpu is None: # if the highest performance is too high and there is no chipset match, just choose the highest performance with a chipset match without price consideration
                    best_perf = 0.0
                    for cpu in cpu_objs:
                        temp_mobo = mobo_objs.filter(chipset=cpu.platform).order_by('price')

                        if temp_mobo:
                            temp_mobo = temp_mobo[0]
                            if cpu.cpu_fan == False:
                                fan = FAN.objects.filter(price__isnull=False).order_by('price')[0]
                                fan_price = fan.price

                            if type_ == 'streaming' and best_perf < cpu.combined_perf:
                                best_perf = cpu.combined_perf
                                best_cpu = cpu
                                best_mobo = mobo
                                best_fan = fan
                                best_fan_price = fan_price
                            elif type_ == 'gaming' and best_perf < cpu.gaming_perf:
                                best_perf = cpu.gaming_perf
                                best_cpu = cpu
                                best_mobo = mobo
                                best_fan = fan
                                best_fan_price = fan_price
                            elif type_ == 'production' and best_perf < cpu.workstation_perf:
                                best_perf = cpu.workstation_perf
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
        mainBudget -= best_cpu.price
        mainBudget -= best_mobo.price
        mainBudget -= best_fan_price
        #######
        # GPU #
        #######
        # for streaming/gaming PCs, gaming performance benchmark used with performance ratio
        # for production, video memory important so considered here (https://nerdtechy.com/workstation-vs-gaming-pc)
        gpu_brands= []
        for brand in brand_preferences:
            if brand == 'nvidia':
                gpu_brands.append('GeForce')
            elif brand == 'AMD':
                gpu_brands.append('Radeon')

        while True:
            # filters gpus based on brand preferences (attempts finding brand matches maximum of twice)
            gpu_objs=GPU.objects.none()
            for brand in gpu_brands:
                gpu_objs = gpu_objs.union(GPU.objects.filter(price__isnull = False,
                                                             chipset__startswith=brand,
                                                             price__lte=mainBudget))
            if not gpu_objs:
                gpu_objs=GPU.objects.filter(price__isnull=False, price__lte=mainBudget)
            if gpu_objs: # if gpus in price range
                best_gpu_perf = gpu_objs.order_by('gaming_perf').reverse()[0].gaming_perf
                best_gpu = None
                best_gpu_mem = 0
                best_gpu_perf_ratio = 0
                for gpu in gpu_objs:
                    if type_ == 'production' and gpu.mem >= best_gpu_mem and gpu.gaming_perf >= best_gpu_perf - 5:
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
        actual_wattage=best_cpu.tdp + best_gpu.tdp + 175
        if overclock:
            actual_wattage+=50
        if pwr.wattage < actual_wattage*.95:
            while True:
                pwr_objs = PWR.objects.filter(price__isnull = False, wattage__gte=actual_wattage).order_by('price')
                            # base power supply
                pwr = pwr_objs[0]
                price_cap = pwr.price * 0.10 + pwr.price

                # Titanium
                pwr_titanium = pwr_objs.filter(rating='80+ Titanium',
                                        price__lte=price_cap).order_by('price')
                if pwr_titanium:
                    pwr = pwr_titanium[0]
                else:
                    # Platinum
                    pwr_platinum = pwr_objs.filter(rating='80+ Platinum',
                                                price__lte=price_cap).order_by('price')
                    if pwr_platinum:
                        pwr = pwr_platinum[0]
                    else:
                        # Gold
                        pwr_gold = pwr_objs.filter(rating='80+ Gold',
                                                    price__lte=price_cap).order_by('price')
                        if pwr_gold:
                            pwr = pwr_gold[0]
                        else:
                            # Silver
                            pwr_silver = pwr_objs.filter(rating='80+ Silver',
                                                    price__lte=price_cap).order_by('price')
                            if pwr_silver:
                                pwr = pwr_silver[0]
                            else:
                                # Bronze
                                pwr_bronze = pwr_objs.filter(rating='80+ Bronze',
                                                            price__lte=price_cap).order_by('price')
                                if pwr_bronze:
                                    pwr = pwr_bronze[0]
                if checkPart(pwr):
                    break
        budget_remaining -= pwr.price
        # Adding CPU, fan, GPU, motherboard, memory, case, and power to parts list
        parts.update({'CPU' : best_cpu, 'FAN' : best_fan, 'GPU' : best_gpu, 'MOBO' : best_mobo, 'MEM' : mem, 'CASE': case_obj, 'PWR' : pwr})
        if best_ssd:
            parts.update({'STORAGE' : best_ssd})
        if best_hdd:
            parts.update({'EXTRA' : best_hdd})
        parts.update({'BUILD COST' : round(starting_budget-budget_remaining,2)})
        return parts
    except AttributeError as e:  # if there is no part at budget given, won't cause crash due to none being found when part.price
        print(e)
        return None
    except IndexError as e: # if there is no part at budget given, won't cause error due to indexing empty list
        print(e)
        return None
