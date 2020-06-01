from django.db import models

class CPU(models.Model):
    name =  models.CharField(max_length=20)
    manufacturer = models.CharField(max_length=10)
    cpu_fan = models.BooleanField()
    cores = models.PositiveSmallIntegerField()
    platform = models.CharField(max_length=50)
    price = models.FloatField()
    gaming_perf = models.PositiveSmallIntegerField()
    tdp = models.PositiveSmallIntegerField()
    links = models.CharField(max_length=1000)
class GPU(models.Model):
    price = models.FloatField()
    gaming_perf = models.PositiveSmallIntegerField()
    manufacturer = models.CharField(max_length=30)
    chipset = models.CharField(max_length=50)
    tdp = models.PositiveSmallIntegerField()
    links = models.CharField(max_length=1000)
class MEM(models.Model):
    name =  models.CharField(max_length=20)
    speed = models.PositiveSmallIntegerField()
    cas = models.PositiveSmallIntegerField()
    modules = models.CharField(max_length=25)
    price = models.FloatField()
    links = models.CharField(max_length=1000)
class STORAGE(models.Model):
    name =  models.CharField(max_length=20)
    capacity = models.IntegerField()
    price = models.FloatField()
    form = models.CharField(max_length=35)
    links = models.CharField(max_length=1000)
class PWR(models.Model):
    name =  models.CharField(max_length=20)
    wattage = models.PositiveSmallIntegerField()
    price = models.FloatField()
    rating = models.CharField(max_length=10)
    links = models.CharField(max_length=1000)
class CASE(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    size = models.CharField(max_length=10)
    links = models.CharField(max_length=1000)
class MOBO(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    chipset = models.CharField(max_length=50)
    links = models.CharField(max_length=1000)
class FAN(models.Model):
    name =  models.CharField(max_length=20)
    price = models.FloatField()
    links = models.CharField(max_length=1000)