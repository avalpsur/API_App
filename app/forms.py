from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
class BusquedaCineForm(forms.Form):
    direccion = forms.CharField(required=False, label='Dirección')
    telefono = forms.CharField(required=False, label='Teléfono')
    email = forms.EmailField(required=False, label='Email')

class BusquedaSalaForm(forms.Form):
    TAMANO_CHOICES = [
        ('PE', 'Pequeña'),
        ('ME', 'Mediana'),
        ('GR', 'Grande'),
    ]
    tamano = forms.ChoiceField(required=False, choices=TAMANO_CHOICES, label='Tamaño de la Sala')
    cine = forms.CharField(required=False, label='ID del Cine')

class BusquedaPeliculaForm(forms.Form):
    titulo = forms.CharField(required=False, label='Título')
    director = forms.CharField(required=False, label='Director')
    fecha_desde = forms.DateField(required=False, label='Fecha Desde')
    fecha_hasta = forms.DateField(required=False, label='Fecha Hasta')