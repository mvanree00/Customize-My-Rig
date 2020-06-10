from django.db import models

class CPU(models.Model):
    name =  models.CharField(max_length=50)
    cpu_fan = models.BooleanField(default=True)
    cores = models.PositiveSmallIntegerField()
    platform = models.CharField(max_length=50,null=True)
    price = models.FloatField()
    gaming_perf = models.PositiveSmallIntegerField(null=True)
    desktop_perf = models.PositiveSmallIntegerField(null=True)
    workstation_perf = models.PositiveSmallIntegerField(null=True)
    tdp = models.PositiveSmallIntegerField()
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class GPU(models.Model):
    price = models.FloatField()
    gaming_perf = models.PositiveSmallIntegerField(null=True)
    manufacturer = models.CharField(max_length=30)
    chipset = models.CharField(max_length=50)
    tdp = models.PositiveSmallIntegerField(null=True)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.manufacturer+' '+self.chipset
class MEM(models.Model):
    name =  models.CharField(max_length=20)
    speed = models.PositiveSmallIntegerField()
    cas = models.PositiveSmallIntegerField()
    modules = models.CharField(max_length=25)
    price = models.FloatField()
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=30, null = True)
    def __str__(self):
        return self.name
class STORAGE(models.Model):
    name =  models.CharField(max_length=20)
    capacity = models.CharField(max_length=20)
    price = models.FloatField()
    form = models.CharField(max_length=20)
    kind = models.CharField(max_length=10)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class PWR(models.Model):
    name =  models.CharField(max_length=20)
    wattage = models.PositiveSmallIntegerField()
    price = models.FloatField()
    rating = models.CharField(max_length=10)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class CASE(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    size = models.CharField(max_length=10)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=30, null = True)
    def __str__(self):
        return self.name
class MOBO(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    chipset = models.CharField(max_length=50)
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class FAN(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    links = models.CharField(max_length=50,null=True)
    img = models.CharField(max_length=100, null=True)
    kind = models.CharField(max_length=20)
    def __str__(self):
        return self.name