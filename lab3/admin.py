from django.contrib import admin
from .models import CarParameter, Car, Manufacturer, CarClass

admin.site.register(CarParameter)
admin.site.register(Car)
admin.site.register(Manufacturer)
admin.site.register(CarClass)
