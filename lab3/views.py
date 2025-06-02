from django.shortcuts import render, redirect
from .models import Car, CarParameter, Manufacturer, CarClass
from .forms import CarForm, CarParameterForm, ManufacturerForm, CarClassForm

def car_list(request):
    cars = Car.objects.all().prefetch_related('parameters', 'car_class', 'manufacturer')
    return render(request, 'lab3/car_list.html', {'cars': cars})

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab3:car_list')
    else:
        form = CarForm()
    return render(request, 'lab3/form.html', {'form': form, 'title': 'Добавить автомобиль'})

def add_car_parameter(request):
    if request.method == 'POST':
        form = CarParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab3:car_parameter_list')  # или куда хочешь
    else:
        form = CarParameterForm()

    return render(request, 'lab3/form.html', {
        'form': form,
        'title': 'Добавить параметр автомобиля'
    })



def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab3:add_car')
    else:
        form = ManufacturerForm()
    return render(request, 'lab3/form.html', {'form': form, 'title': 'Добавить производителя'})

def add_car_class(request):
    if request.method == 'POST':
        form = CarClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab3:add_car')
    else:
        form = CarClassForm()
    return render(request, 'lab3/form.html', {'form': form, 'title': 'Добавить класс автомобиля'})
