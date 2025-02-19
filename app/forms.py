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

class ClientePost(forms.Form):
    dni = forms.CharField(required=True, label='DNI',
                          max_length=9,
                          min_length=9)
    nombre = forms.CharField(required=True, label='Nombre',
                             max_length=50,
                             min_length=2,
                             help_text="Introduce tu nombre")
    apellidos = forms.CharField(required=True, label='Apellidos',
                                max_length=100,
                                min_length=2,
                                help_text="Introduce tus apellidos")    
    email = forms.EmailField(required=True, label='Email',
                             max_length=100,
                             min_length=2,
                             help_text="Introduce tu email")
    
    def __init__(self, *args, **kwargs):
        super(ClientePost, self).__init__(*args, **kwargs) 
        self.fields['dni'].widget.attrs.update({'class' : 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
        self.fields['apellidos'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
    
class ClienteEditarForm(forms.Form):
    dni = forms.CharField(
        required=True,
        label='DNI',
        max_length=9,
        min_length=9,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    nombre = forms.CharField(
        required=True,
        label='Nombre',
        max_length=50,
        min_length=2,
        help_text="Introduce tu nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellidos = forms.CharField(
        required=True,
        label='Apellidos',
        max_length=100,
        min_length=2,
        help_text="Introduce tus apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        max_length=100,
        min_length=2,
        help_text="Introduce tu email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(ClienteEditarForm, self).__init__(*args, **kwargs)

class ClienteActualizarNombreForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, label="Nuevo Nombre")



class SalaForm(forms.Form):
    TAMANO_CHOICES = [
        ('PE', 'Pequeña'),
        ('ME', 'Mediana'),
        ('GR', 'Grande'),
    ]
    tamano = forms.ChoiceField(required=True, choices=TAMANO_CHOICES, label='Tamaño de la Sala')
    cine = forms.ChoiceField(required=True, label='Cine', choices=[])
    empleado = forms.MultipleChoiceField(required=True, label='Empleados', choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        cines_disponibles = kwargs.pop("cines_disponibles", [])
        empleados_disponibles = kwargs.pop("empleados_disponibles", [])
        
        super(SalaForm, self).__init__(*args, **kwargs)

        self.fields["cine"].choices = [(cine["id"], cine["direccion"]) for cine in cines_disponibles]
        self.fields["empleado"].choices = [(empleado["id"], f"{empleado['nombre']} {empleado['apellidos']}") for empleado in empleados_disponibles]

        self.fields["tamano"].widget.attrs.update({'class': 'form-control'})
        self.fields["cine"].widget.attrs.update({'class': 'form-control'})
        self.fields["empleado"].widget.attrs.update({'class': 'form-control'})
