from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClientePost(forms.Form):
    dni = forms.CharField(max_length=9)
    nombre = forms.CharField(max_length=255)
    apellidos = forms.CharField(max_length=255)
    email = forms.EmailField()

class ClienteEditarForm(forms.Form):
    dni = forms.CharField(max_length=9)
    nombre = forms.CharField(max_length=255)
    apellidos = forms.CharField(max_length=255)
    email = forms.EmailField()

class ClienteActualizarNombreForm(forms.Form):
    nombre = forms.CharField(max_length=255)

class SalaForm(forms.Form):
    TAMANO_CHOICES = [
        ('PE', 'Pequeña'),
        ('ME', 'Mediana'),
        ('GR', 'Grande'),
    ]
    tamano = forms.ChoiceField(choices=TAMANO_CHOICES, label='Tamaño de la Sala')
    cine = forms.ChoiceField(label='Cine')
    empleado = forms.MultipleChoiceField(label='Empleados', required=False)

    def __init__(self, *args, **kwargs):
        cines_disponibles = kwargs.pop('cines_disponibles', [])
        empleados_disponibles = kwargs.pop('empleados_disponibles', [])
        super(SalaForm, self).__init__(*args, **kwargs)
        self.fields['cine'].choices = [(cine['id'], cine['nombre']) for cine in cines_disponibles]
        self.fields['empleado'].choices = [(empleado['id'], empleado['nombre']) for empleado in empleados_disponibles]

class PeliculaForm(forms.Form):
    titulo = forms.CharField(max_length=255)
    director = forms.CharField(max_length=255)
    sinopsis = forms.CharField(widget=forms.Textarea)
    fechaLanzamiento = forms.DateField()
    tiempoProyectada = forms.DurationField(required=False)
    sala = forms.MultipleChoiceField(label='Salas', required=False)

    def __init__(self, *args, **kwargs):
        salas_disponibles = kwargs.pop('salas_disponibles', [])
        super(PeliculaForm, self).__init__(*args, **kwargs)
        self.fields['sala'].choices = [(sala['id'], sala['nombre']) for sala in salas_disponibles]

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


class RegistroForm(UserCreationForm):
    roles = (
        (2, 'cliente'),
        (3,'empleado'),
        (4,'gerente'),        
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','rol']


class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())