from homepage.models import *
from django.db.models import Max
from links import getLink

def getBuild(startingBudget):
    #links = {} <<<<<<<<<<<<<<<<< NOTE THAT LINKS DOESN'T WORK COMPLETELY WITH NON-UPDATED PRICES >>>>>>>>>>>>>>>>>>
    budget = startingBudget
    temp = CPU.objects.filter(price__lte=startingBudget*.2).aggregate(mx = Max('gaming_perf'))
    CPUobj = CPU.objects.filter(price__lte=startingBudget*.2,gaming_perf=temp['mx']).order_by('price')[0]
    if CPUobj.cpu_fan == False:
        FANobj = FAN.objects.filter()[0]
        budget-=FANobj.price
    budget-=CPUobj.price
    temp = GPU.objects.filter(price__lte=startingBudget*.4).aggregate(mx = Max('gaming_perf'))
    GPUobj = GPU.objects.filter(price__lte=startingBudget*.4,gaming_perf=temp['mx']).order_by('price')[0]
    budget-=GPUobj.price
    minPwr = (CPUobj.tdp + GPUobj.tdp + 175)
    PWRobj = PWR.objects.filter(wattage__gte=minPwr).order_by('price')[0]
    budget-=PWRobj.price
    MOBOobj = MOBO.objects.filter(chipset=CPUobj.platform).order_by('price')[0]
    budget-=MOBOobj.price
    CASEobj = CASE.objects.order_by('price')[0]
    budget-=CASEobj.price
    if startingBudget>=1200:
        MEMobj = MEM.objects.filter(modules='32 GB').order_by('price')[0]
    elif startingBudget>=700:
        MEMobj = MEM.objects.filter(modules='16 GB').order_by('price')[0]
    else:
        MEMobj = MEM.objects.filter(modules=' 8 GB').order_by('price')[0]
    budget-=MEMobj.price
    temp = STORAGE.objects.filter(price__lte=budget,kind='SSD').aggregate(mx = Max('capacity'))
    STORAGEobj = STORAGE.objects.filter(price__lte=budget,kind='SSD',capacity__gte=temp['mx']*.95).order_by('price')[0]
    budget-=STORAGEobj.price
    if budget>30: # extra storage (HDD)
        temp = STORAGE.objects.filter(price__lte=budget).aggregate(mx = Max('capacity'))
        EXTRAobj = STORAGE.objects.filter(price__lte=budget,capacity__gte=temp['mx']*.95).order_by('price')[0]
        budget-=EXTRAobj.price
        print(EXTRAobj,EXTRAobj.capacity,EXTRAobj.price)
        #links.update({'EXTRA' : getLink(EXTRAobj.links)})
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
    print('Total Build:',startingBudget-round(budget,2))
    #print(links)