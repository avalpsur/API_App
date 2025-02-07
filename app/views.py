from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError
from datetime import timedelta


import requests
from pathlib import Path

# Create your views here.

import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()
EMPLEADO_KEY = env('EMPLEADO_KEY')
CLIENTE_KEY = env('CLIENTE_KEY')
GERENTE_KEY = env('GERENTE_KEY')



def index(request):
    if not "fecha_inicio" in request.session:
        #request.session["fecha_inicio"] = timezone.now().strftime('%d/%m/%Y %H:%M')
        request.session['variable1'] ='Cines Polígono Sur'
        request.session['variable2'] = '2025'
        request.session['variable3'] = 'C/ Esclava del Señor, 1'
        request.session['variable4'] = '41013'
    return render(request, 'index.html')


def clientes_lista_api(request):
    headers = {'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4OTMyMjM3LCJpYXQiOjE3Mzg5MzE5MzcsImp0aSI6Ijc1NjVlNDcwNDQyNzQxMTc4NGUxNjA1NmM4MzRmYTFjIiwidXNlcl9pZCI6Mn0.XcV1dGgs15spKRnvc3qDjzcYQRr2irJNL3LP55Fg7vQ'}
    response = requests.get('https://avalpsur.pythonanywhere.com/api/v1/clientes',headers=headers)
    clientes = response.json()
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def salas_lista_api(request):
    headers = {'Authorization' : f'Bearer {CLIENTE_KEY}'}
    response = requests.get('https://avalpsur.pythonanywhere.com/api/v1/salas',headers=headers)
    salas = response.json()
    return render(request, 'sala/lista_api.html',{"salas_mostrar":salas})

def peliculas_lista_api(request):
    headers = {'Authorization' : f'Bearer {EMPLEADO_KEY}'}
    response = requests.get('https://avalpsur.pythonanywhere.com/api/v1/peliculas',headers=headers)
    peliculas = response.json()
    return render(request, 'pelicula/lista_api.html',{"peliculas_mostrar":peliculas})

def cines_lista_api(request):
    headers = {'Authorization' : f'Bearer {GERENTE_KEY}'}
    response = requests.get('https://avalpsur.pythonanywhere.com/api/v1/cines',headers=headers)
    cines = response.json()
    return render(request, 'cine/lista_api.html',{"cine_mostrar":cines})


def cliente_busqueda(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get('http://127.0.0.1:8000/api/v1/clientes/buscar',
                                headers=headers,
                                params=formulario.cleaned_data
                                )
        clientes = response.json()
        return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect('index')


def cine_busqueda(request):
    if(len(request.GET) > 0):
        formulario = BusquedaCineForm(request.GET)
    
        try:
            headers = crear_cabecera()
            response = requests.get(
                                    'http://127.0.0.1:8000/api/v1/clientes/buscar',
                                    headers=headers,
                                    params=formulario.cleaned_data
                                    )
            if(response.status_code == requests.codes.ok):
                cines = response.json()
                return render(request, 'cine/lista_api.html',{"cine_mostrar":cines})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
            return render(request, 'cine/busqueda.html',{"formulario":formulario})
        except Exception as err:
            print(f'Hubo un error: {err}')
            return mi_error_500(request)
   
        
def crear_cabecera():
    return {'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4OTMyMjM3LCJpYXQiOjE3Mzg5MzE5MzcsImp0aSI6Ijc1NjVlNDcwNDQyNzQxMTc4NGUxNjA1NmM4MzRmYTFjIiwidXNlcl9pZCI6Mn0.XcV1dGgs15spKRnvc3qDjzcYQRr2irJNL3LP55Fg7vQ'}


