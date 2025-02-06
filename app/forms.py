from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)