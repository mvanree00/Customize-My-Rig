from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(GPU)
admin.site.register(CPU)
admin.site.register(FAN)
admin.site.register(MOBO)
admin.site.register(MEM)
admin.site.register(STORAGE)
admin.site.register(CASE)
admin.site.register(PWR)