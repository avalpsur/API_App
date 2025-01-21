from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError

import requests
import environ
import os
from pathlib import Path

# Create your views here.

def index(request):
    if not "fecha_inicio" in request.session:
        request.session["fecha_inicio"] = timezone.now().strftime('%d/%m/%Y %H:%M')
        request.session['variable1'] ='Cines Polígono Sur'
        request.session['variable2'] = '2025'
        request.session['variable3'] = 'C/ Esclava del Señor, 1'
        request.session['variable4'] = '41013'
    return render(request, 'index.html')


def clientes_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/clientes')
    clientes = response.json()
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def salas_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/salas')
    salas = response.json()
    return render(request, 'sala/lista_api.html',{"salas_mostrar":salas})

def peliculas_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/peliculas')
    peliculas = response.json()
    return render(request, 'pelicula/lista_api.html',{"peliculas_mostrar":peliculas})
