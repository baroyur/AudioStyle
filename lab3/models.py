from django.db import models

class CarClass(models.Model):
    name = models.CharField(max_length=100, verbose_name='Класс автомобиля')

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Производитель')

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100, verbose_name='Автомобиль')
    car_class = models.ForeignKey(CarClass, on_delete=models.CASCADE, related_name='cars', verbose_name='Класс автомобиля')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='cars', verbose_name='Производитель')

    def __str__(self):
        return f"{self.manufacturer} {self.name}"

class CarParameter(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='parameters', verbose_name='Автомобиль')
    key = models.CharField(max_length=100, verbose_name='Параметр')
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f"{self.key}: {self.value}"
