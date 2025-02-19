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
        
        request.session['variable1'] ='Cines Polígono Sur'
        request.session['variable2'] = '2025'
        request.session['variable3'] = 'C/ Esclava del Señor, 1'
        request.session['variable4'] = '41013'
    return render(request, 'index.html')

#Creamos una función para cambiar la url de la API en caso de que cambie la versión
def obtener_url():
    return "https://avalpsur.pythonanywhere.com/api/v1/"

def procesar_respuesta(response):
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return response.json()
    elif 'application/xml' in content_type or 'text/xml' in content_type:
        import xml.etree.ElementTree as ET
        return ET.fromstring(response.text)
    else:
        return response.text

def clientes_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/clientes',headers=headers)
    clientes = procesar_respuesta(response)
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def salas_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/salas',headers=headers)
    salas = procesar_respuesta(response)
    return render(request, 'sala/lista_api.html',{"salas_mostrar":salas})

def peliculas_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/peliculas',headers=headers)
    peliculas = procesar_respuesta(response)
    return render(request, 'pelicula/lista_api.html',{"peliculas_mostrar":peliculas})

def cines_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/cines',headers=headers)
    cines = procesar_respuesta(response)
    return render(request, 'cine/lista_api.html',{"cine_mostrar":cines})


def cliente_busqueda(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get('http://127.0.0.1:8000/api/v1/clientes/buscar',
                                headers=headers,
                                params=formulario.cleaned_data
                                )
        clientes = procesar_respuesta(response)
        return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect('index')


def cine_busqueda(request):
    if len(request.GET) > 0:
        formulario = BusquedaCineForm(request.GET)
        
        if formulario.is_valid():  
            try:
                headers = crear_cabecera()
                response = requests.get(
                    'http://127.0.0.1:8000/api/v1/cines/buscar',
                    headers=headers,
                    params=formulario.cleaned_data
                )
                if response.status_code == requests.codes.ok:
                    cines = procesar_respuesta(response)
                    return render(request, 'cine/lista_api.html', {"cine_mostrar": cines})
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = procesar_respuesta(response)
                    for error in errores:
                        formulario.add_error(error, errores[error])
                return render(request, 'cine/busqueda_avanzada.html', {"formulario": formulario})
            except Exception as err:
                print(f'Hubo un error: {err}')
                return mi_error_500(request)
        else:
            print("Formulario no válido")
            return render(request, 'cine/busqueda_avanzada.html', {"formulario": formulario})

    return render(request, 'cine/busqueda_avanzada.html', {"formulario": BusquedaCineForm()})


def sala_busqueda(request):
    formulario = BusquedaSalaForm(request.GET if request.GET else None)  # Asegura que siempre haya un formulario
    
    if request.GET:
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/salas/buscar',
                headers=headers,
                params=formulario.data
            )             
            if response.status_code == requests.codes.ok:
                salas = procesar_respuesta(response)
                return render(request, 'sala/lista_busqueda.html', {"salas_mostrar": salas, "formulario": formulario})
            else:
                response.raise_for_status()
        except HTTPError as http_err:
            return render(request, 'sala/busqueda_avanzada.html', {"formulario": formulario, "error": f"Error en la petición: {http_err}"})
        except Exception as err:
            return render(request, 'sala/busqueda_avanzada.html', {"formulario": formulario, "error": f"Error inesperado: {err}"})
    
    return render(request, 'sala/busqueda_avanzada.html', {"formulario": formulario})

def pelicula_busqueda(request):
    if len(request.GET) > 0:
        formulario = BusquedaPeliculaForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/peliculas/buscar',  
                headers=headers,
                params=formulario.data
            )

            
            if response.status_code == requests.codes.ok:
                peliculas = procesar_respuesta(response)
                return render(request, 'pelicula/lista_avanzada.html',
                              {"peliculas_mostrar": peliculas})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = procesar_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'pelicula/busqueda_avanzada_datepicker.html',
                              {"formulario": formulario, "errores": errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaPeliculaForm(None)
    return render(request, 'pelicula/busqueda_avanzada_datepicker.html', {"formulario": formulario})


def cliente_post(request):
    if request.method == 'POST':
        try:
            formulario = ClientePost(request.POST)  # Cargar los datos en el formulario
            headers = crear_cabecera()  # Encabezados para la API
            datos = formulario.data.copy()

            # Asegurar que todos los datos están en el diccionario
            datos["dni"] = request.POST.get("dni")
            datos["nombre"] = request.POST.get("nombre")
            datos["apellidos"] = request.POST.get("apellidos")
            datos["email"] = request.POST.get("email")

            # Hacer la petición POST a la API
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/clientes/create',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == 201:  # 201 Created
                messages.success(request, "Cliente creado con éxito")
                return redirect('cliente_lista')  # Redirigir a la lista de clientes

            else:
                print("Error en la respuesta:", response.status_code)
                response.raise_for_status()

        except HTTPError as http_err:
            print(f'Error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'cliente/create.html', {"formulario": formulario})
            else:
                return mi_error_500(request)

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return mi_error_500(request)

    else:
        formulario = ClientePost(None)

    return render(request, 'cliente/create.html', {"formulario": formulario})


def cliente_editar(request, cliente_id):
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    headers = crear_cabecera()
    response = requests.get(f'http://127.0.0.1:8000/api/v1/clientes/{cliente_id}', headers=headers)

    if response.status_code != requests.codes.ok:
        return mi_error_500(request)

    cliente = response.json()

    formulario = ClienteEditarForm(datosFormulario, initial={
        'dni': cliente['dni'],
        'nombre': cliente['nombre'],
        'apellidos': cliente['apellidos'],
        'email': cliente['email']
    })

    if request.method == "POST":
        formulario = ClienteEditarForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            response = requests.put(
                f'http://127.0.0.1:8000/api/v1/clientes/{cliente_id}/editar',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                return redirect("cliente_lista")
            else:
                print(response.status_code)
                response.raise_for_status()

    return render(request, 'cliente/editar.html', {"formulario": formulario, "cliente": cliente})

def cliente_editar_nombre(request, cliente_id):
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    headers = crear_cabecera()

    response = requests.get(f'http://127.0.0.1:8000/api/v1/clientes/{cliente_id}', headers=headers)

    if response.status_code != requests.codes.ok:
        messages.error(request, "No se pudo obtener el cliente")
        return redirect("cliente_lista")

    cliente = response.json()

    formulario = ClienteActualizarNombreForm(datosFormulario, initial={
        'nombre': cliente['nombre']
    })

    if request.method == "POST":
        formulario = ClienteActualizarNombreForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()

            response = requests.patch(
                f'http://127.0.0.1:8000/api/v1/clientes/{cliente_id}/actualizar/nombre',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, "Nombre actualizado con éxito")
                return redirect("cliente_lista")  # Redirigir a la lista de clientes
            else:
                response.raise_for_status()

    return render(request, 'cliente/actualizar_nombre.html', {"formulario": formulario, "cliente": cliente})


def cliente_eliminar(request, cliente_id):
    try:
        headers = crear_cabecera() 
        response = requests.delete(
            f'http://127.0.0.1:8000/api/v1/clientes/{cliente_id}/eliminar',
            headers=headers,
        )

        if response.status_code == requests.codes.ok:
            messages.success(request, "Cliente eliminado correctamente")
            return redirect("cliente_lista")  
        else:
            response.raise_for_status()

    except HTTPError as http_err:
        messages.error(request, f"Error en la petición: {http_err}")
    except Exception as err:
        messages.error(request, f"Ocurrió un error inesperado: {err}")
        return mi_error_500(request)

    return redirect("cliente_lista") 



def sala_crear(request):
    headers =crear_cabecera()   

    # Obtener cines desde la API
    response_cines = requests.get('http://127.0.0.1:8000/api/v1/cines', headers=headers)
    cines_disponibles = response_cines.json() if response_cines.status_code == 200 else []

    # Obtener empleados desde la API
    response_empleados = requests.get('http://127.0.0.1:8000/api/v1/empleados', headers=headers)
    empleados_disponibles = response_empleados.json() if response_empleados.status_code == 200 else []

    if request.method == "POST":
        try:
            formulario = SalaForm(request.POST, cines_disponibles=cines_disponibles, empleados_disponibles=empleados_disponibles)
            if formulario.is_valid():
                datos = formulario.cleaned_data.copy()
                datos["cine"] = int(datos["cine"])  # Asegurar que cine se pasa como ID
                datos["empleado"] = list(map(int, request.POST.getlist("empleado")))  # Convertir empleados a lista de IDs
                
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/salas/create',
                    headers=headers,
                    json=datos
                )

                if response.status_code == 201:
                    messages.success(request, "Sala creada con éxito")
                    return redirect("sala_lista")
                else:
                    print(f"Error en la respuesta: {response.status_code}")
                    response.raise_for_status()
                    
        except HTTPError as http_err:
            print(f'Error en la petición: {http_err}')
        except Exception as err:
            print(f'Ocurrió un error: {err}')

    else:
        formulario = SalaForm(cines_disponibles=cines_disponibles, empleados_disponibles=empleados_disponibles)

    return render(request, 'sala/create.html', {"formulario": formulario, "cines": cines_disponibles, "empleados": empleados_disponibles})

def crear_cabecera():
    return {'Authorization' : 'Bearer aTDC2VfZVr0tyDS1r9HoN2BcAEPp8d',
            "Content-Type": "application/json"
            }


#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)