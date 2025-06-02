from django import forms
from .models import CarClass, Manufacturer, Car, CarParameter

class CarClassForm(forms.ModelForm):
    class Meta:
        model = CarClass
        fields = ['name']

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_class', 'manufacturer', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'car_class': forms.Select(attrs={'class': 'form-input'}),
            'manufacturer': forms.Select(attrs={'class': 'form-input'}),
        }

class CarParameterForm(forms.ModelForm):
    class Meta:
        model = CarParameter
        fields = ['car', 'key', 'value']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-input'}),
            'key': forms.TextInput(attrs={'class': 'form-input'}),
            'value': forms.TextInput(attrs={'class': 'form-input'}),
        }
