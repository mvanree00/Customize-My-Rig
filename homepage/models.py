from django.db import models

class CPU(models.Model):
    name =  models.CharField(max_length=50)
    cpu_fan = models.BooleanField(default=True)
    cores = models.PositiveSmallIntegerField()
    platform = models.CharField(max_length=50,null=True)
    price = models.FloatField()
    gaming_perf = models.PositiveSmallIntegerField(null=True)
    tdp = models.PositiveSmallIntegerField()
    links = models.CharField(max_length=1000,null=True) # if oos take next site
    def __str__(self):
        return self.name
class GPU(models.Model):
    price = models.FloatField()
    gaming_perf = models.PositiveSmallIntegerField(null=True)
    manufacturer = models.CharField(max_length=30)
    chipset = models.CharField(max_length=50)
    tdp = models.PositiveSmallIntegerField(null=True)
    links = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.manufacturer+' '+self.chipset
class MEM(models.Model):
    name =  models.CharField(max_length=20)
    speed = models.PositiveSmallIntegerField()
    cas = models.PositiveSmallIntegerField()
    modules = models.CharField(max_length=25)
    price = models.FloatField()
    links = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.name
class STORAGE(models.Model):
    name =  models.CharField(max_length=20)
    capacity = models.IntegerField()
    price = models.FloatField()
    form = models.CharField(max_length=20)
    kind = models.CharField(max_length=10)
    links = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.name
class PWR(models.Model):
    name =  models.CharField(max_length=20)
    wattage = models.PositiveSmallIntegerField()
    price = models.FloatField()
    rating = models.CharField(max_length=10)
    links = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.name
class CASE(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    size = models.CharField(max_length=10)
    links = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.name
class MOBO(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    chipset = models.CharField(max_length=50)
    links = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.name
class FAN(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    links = models.CharField(max_length=1000,null=True)
    kind = models.CharField(max_length=20)
    def __str__(self):
        return self.name