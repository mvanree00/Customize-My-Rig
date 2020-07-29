from django.db import models

class CPU(models.Model): # add in core/boost clocks?
    name =  models.CharField(max_length=50)
    cpu_fan = models.BooleanField(default=True)
    cores = models.PositiveSmallIntegerField()
    platform = models.CharField(max_length=50,null=True)
    price = models.FloatField(null=True)
    gaming_perf = models.PositiveSmallIntegerField(null=True)
    desktop_perf = models.PositiveSmallIntegerField(null=True)
    workstation_perf = models.PositiveSmallIntegerField(null=True)
    tdp = models.PositiveSmallIntegerField()
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    combined_perf = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return self.name
class GPU(models.Model): # add in core/boost clocks?
    price = models.FloatField(null=True)
    mem = models.PositiveSmallIntegerField(null=True)
    gaming_perf = models.PositiveSmallIntegerField(null=True)
    manufacturer = models.CharField(max_length=50)
    chipset = models.CharField(max_length=50)
    tdp = models.PositiveSmallIntegerField(null=True)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.manufacturer+' '+self.chipset
class MEM(models.Model):
    name =  models.CharField(max_length=20)
    speed = models.PositiveSmallIntegerField()
    cas = models.PositiveSmallIntegerField()
    modules = models.CharField(max_length=25)
    price = models.FloatField(null=True)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=30, null = True)
    webpage = models.CharField(max_length=125,null=True)
    realspeed = models.FloatField(null=True)
    speedperdollar = models.PositiveSmallIntegerField(null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
class STORAGE(models.Model):
    name =  models.CharField(max_length=20)
    capacity = models.PositiveSmallIntegerField()
    price = models.FloatField(null=True)
    form = models.CharField(max_length=20)
    kind = models.CharField(max_length=10)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
class PWR(models.Model):
    name =  models.CharField(max_length=20)
    wattage = models.PositiveSmallIntegerField()
    price = models.FloatField(null=True)
    rating = models.CharField(max_length=10)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
class CASE(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField(null=True)
    size = models.CharField(max_length=10)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=30, null = True)
    panel = models.BooleanField(default=False)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
class MOBO(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField(null=True)
    chipset = models.CharField(max_length=50)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
class FAN(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField(null=True)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=110, null=True)
    kind = models.CharField(max_length=20)
    webpage = models.CharField(max_length=125,null=True)
    last_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name

class BUILD(models.Model):
    build_ID = models.IntegerField(null=True)
    build_Cost = models.FloatField(null=True)
    CPU_links = models.CharField(max_length=50, null=True)
    GPU_links = models.CharField(max_length=50, null=True)
    MEM_links = models.CharField(max_length=50, null=True)
    STORAGE_links = models.CharField(max_length=50, null=True)
    EXTRA_links = models.CharField(max_length=50, null=True)
    PWR_links = models.CharField(max_length=50, null=True)
    CASE_links = models.CharField(max_length=50, null=True)
    MOBO_links = models.CharField(max_length=50, null=True)
    FAN_links = models.CharField(max_length=50, null=True)
    def __str__(self):
        return str(self.build_ID)
