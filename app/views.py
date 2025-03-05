from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
import json
from requests.exceptions import HTTPError
from datetime import timedelta
import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


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
    response = requests.get('http://127.0.0.1:8000/api/v1/clientes', headers=headers)
    clientes = procesar_respuesta(response)
    return render(request, 'cliente/lista_api.html', {"clientes_mostrar": clientes})

def salas_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/salas', headers=headers)
    salas = procesar_respuesta(response)
    return render(request, 'sala/lista_api.html', {"salas_mostrar": salas})

def peliculas_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/peliculas', headers=headers)
    peliculas = procesar_respuesta(response)
    return render(request, 'pelicula/lista_api.html', {"peliculas_mostrar": peliculas})

def cines_lista_api(request):
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/cines', headers=headers)
    cines = procesar_respuesta(response)
    return render(request, 'cine/lista_api.html', {"cine_mostrar": cines})


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
            formulario = ClientePost(request.POST) 
            headers = crear_cabecera()  
            datos = formulario.data.copy()

            datos["dni"] = request.POST.get("dni")
            datos["nombre"] = request.POST.get("nombre")
            datos["apellidos"] = request.POST.get("apellidos")
            datos["email"] = request.POST.get("email")

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

    return render(request, 'cliente/actualizar.html', {"formulario": formulario, "cliente": cliente})

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
    headers = crear_cabecera()   

    response_cines = requests.get('http://127.0.0.1:8000/api/v1/cines', headers=headers)
    cines_disponibles = response_cines.json() if response_cines.status_code == 200 else []

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
            else:
                messages.error(request, "Formulario no válido")
        except HTTPError as http_err:
            print(f'Error en la petición: {http_err}')
            messages.error(request, f"Error en la petición: {http_err}")
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            messages.error(request, f"Ocurrió un error: {err}")

    else:
        formulario = SalaForm(cines_disponibles=cines_disponibles, empleados_disponibles=empleados_disponibles)

    return render(request, 'sala/create.html', {"formulario": formulario, "cines": cines_disponibles, "empleados": empleados_disponibles})


def sala_editar(request, sala_id):
    sala = obtener_sala(sala_id)
    
    if not sala:
        messages.error(request, "La sala no existe.")
        return redirect('sala_lista')
    
    # Obtener opciones de cines y empleados para el formulario
    cines = obtener_cines()
    empleados = obtener_empleados()

    # Inicializando el formulario con los datos de la sala
    formulario = SalaForm(
        request.POST or None,
        initial={
            'tamano': sala['tamano'],
            'cine': sala['cine'],
            'empleado': [empleado['id'] for empleado in sala['empleado']]
        }
    )

    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data
        datos["cine"] = int(datos["cine"])  # Asegura que se pasa el ID del cine
        datos["empleado"] = list(map(int, request.POST.getlist("empleado")))

        headers = crear_cabecera()
        
        try:
            response = requests.put(
                f'http://127.0.0.1:8000/api/v1/salas/{sala_id}/editar',
                headers=headers,
                json=datos
            )

            if response.status_code == 200:
                messages.success(request, "Sala editada con éxito.")
                return redirect('sala_lista')
            else:
                messages.error(request, f"Error al editar la sala: {response.status_code}")
                response.raise_for_status()
        except HTTPError as http_err:
            messages.error(request, f"Error en la petición: {http_err}")
        except Exception as err:
            messages.error(request, f"Ocurrió un error: {err}")

    return render(request, 'sala/editar.html', {
        "formulario": formulario,
        "sala": sala,
        "cines": cines,  # Pasamos los cines al contexto
        "empleados": empleados  # Pasamos los empleados al contexto
    })

def sala_actualizar_tamano(request, sala_id):
    sala = obtener_sala(sala_id)
    if request.method == "POST":
        headers = crear_cabecera()
        datos = {'tamano': request.POST.get('tamano')}
        
        response = requests.patch(
            f'http://127.0.0.1:8000/api/v1/salas/{sala_id}/actualizar/tamano',
            headers=headers,
            data=json.dumps(datos)
        )

        if response.status_code == 200:
            messages.success(request, "Tamaño de la sala actualizado con éxito.")
            return redirect('sala_lista')
        else:
            messages.error(request, "Error al actualizar el tamaño de la sala.")
            response.raise_for_status()
    
    return render(request, 'sala/actualizar_tamano.html', {"sala": sala})
def sala_eliminar(request, sala_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'http://127.0.0.1:8000/api/v1/salas/{sala_id}/eliminar',
            headers=headers,
        )
        if response.status_code == 200:
            messages.success(request, "Sala eliminada correctamente.")
            return redirect("sala_lista")
        else:
            messages.error(request, "Error al eliminar la sala.")
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        messages.error(request, f"Ocurrió un error: {err}")
        return mi_error_500(request)

def pelicula_crear(request):
    headers = crear_cabecera()
    salas_disponibles = obtener_salas()

    if request.method == 'POST':
        try:
            formulario = PeliculaForm(request.POST, salas_disponibles=salas_disponibles)
            if formulario.is_valid():
                datos = formulario.cleaned_data
                datos['sala'] = list(map(int, request.POST.getlist('sala')))
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/peliculas/create',
                    headers=headers,
                    json=datos
                )
                if response.status_code == 201:
                    messages.success(request, "Película creada con éxito")
                    return redirect('pelicula_lista')
                else:
                    response.raise_for_status()
            else:
                messages.error(request, "Formulario no válido")
        except HTTPError as http_err:
            messages.error(request, f"Error en la petición: {http_err}")
        except Exception as err:
            messages.error(request, f"Ocurrió un error: {err}")
    else:
        formulario = PeliculaForm(salas_disponibles=salas_disponibles)
    return render(request, 'pelicula/create.html', {"formulario": formulario})


def pelicula_editar(request, pelicula_id):
    if request.method == "POST":
        try:
            formulario = PeliculaForm(request.POST)
            headers = crear_cabecera()

            if formulario.is_valid():
                datos = formulario.cleaned_data.copy()
                datos["sala"] = request.POST.getlist("sala")
                datos["fechaLanzamiento"] = datos["fechaLanzamiento"].isoformat()

                # 🔥 Conversión de timedelta a cadena HH:MM:SS
                if formulario.cleaned_data["tiempoProyectada"]:
                    tiempo = formulario.cleaned_data["tiempoProyectada"]
                    datos["tiempoProyectada"] = str(timedelta(seconds=tiempo.total_seconds()))
                else:
                    datos["tiempoProyectada"] = None
                
                # Debugging: Muestra los datos que se van a enviar
                print("🔍 Datos que se enviarán en el PUT:", datos)

                # Enviar la petición a la API
                response = requests.put(
                    f'http://127.0.0.1:8000/api/v1/peliculas/{pelicula_id}/editar',
                    headers=headers,
                    data=json.dumps(datos)
                )

                if response.status_code == 200:
                    messages.success(request, "Película editada con éxito.")
                    return redirect("pelicula_lista")
                else:
                    print(f"Error en la respuesta: {response.status_code}")
                    response.raise_for_status()
        except HTTPError as http_err:
            print(f'Error en la petición: {http_err}')
            return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        headers = crear_cabecera()
        response = requests.get(f'http://127.0.0.1:8000/api/v1/peliculas/{pelicula_id}', headers=headers)
        if response.status_code == 200:
            pelicula = response.json()
            formulario = PeliculaForm(initial={
                'titulo': pelicula['titulo'],
                'director': pelicula['director'],
                'sinopsis': pelicula['sinopsis'],
                'fechaLanzamiento': pelicula['fechaLanzamiento'],
                'tiempoProyectada': pelicula['tiempoProyectada'],
                # ⚠️ Aquí está el cambio
                'sala': pelicula['sala']
            })
        else:
            return mi_error_500(request)

    return render(request, 'pelicula/editar.html', {
        "formulario": formulario,
        "pelicula": pelicula
    })



def pelicula_actualizar_nombre(request, pelicula_id):
    if request.method == "POST":
        try:
            headers = crear_cabecera()
            datos = {
                "nombre": request.POST.get("nombre")
            }
            
            response = requests.patch(
                f'http://127.0.0.1:8000/api/v1/peliculas/{pelicula_id}/actualizar/nombre',
                headers=headers,
                data=json.dumps(datos)
            )
            
            if response.status_code == 200:
                messages.success(request, "Nombre de la película actualizado con éxito")
                return redirect("pelicula_lista")
            else:
                response.raise_for_status()
        
        except HTTPError as http_err:
            print(f'Error en la petición: {http_err}')
            return mi_error_500(request)
        
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

def pelicula_eliminar(request, pelicula_id):
    try:
        headers = crear_cabecera()
        
        response = requests.delete(
            f'http://127.0.0.1:8000/api/v1/peliculas/{pelicula_id}/eliminar',
            headers=headers
        )
        
        if response.status_code == 204:
            messages.success(request, "Película eliminada con éxito")
            return redirect("pelicula_lista")
        else:
            response.raise_for_status()
        
    except HTTPError as http_err:
        print(f'Error en la petición: {http_err}')
        return mi_error_500(request)
    
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)

def obtener_pelicula(pelicula_id):
    headers = crear_cabecera()
    url = f'http://127.0.0.1:8000/api/v1/peliculas/{pelicula_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener la película: {response.status_code}")
        return None

def obtener_salas():
    headers = crear_cabecera()
    url = 'http://127.0.0.1:8000/api/v1/salas'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener salas:", response.status_code)
        return []
    
def obtener_sala(sala_id):
    headers = crear_cabecera()
    url = f'http://127.0.0.1:8000/api/v1/salas/{sala_id}'
    
    response = requests.get(url, headers=headers)
    
    print("STATUS:", response.status_code)
    print("JSON:", response.json())  # 👈 Esto imprimirá el contenido de la respuesta
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener la sala: {response.status_code}")
        return None

def obtener_cines():
    headers = crear_cabecera()
    url = 'http://127.0.0.1:8000/api/v1/cines'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener cines:", response.status_code)
        return []

def obtener_empleados():
    headers = crear_cabecera()
    url = 'http://127.0.0.1:8000/api/v1/empleados'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener empleados:", response.status_code)
        return []

def crear_cabecera():
        return {
            'Authorization': 'Bearer aJb68cGMEWVgMYKkZdAEzWA9YEmRwK',
            "Content-Type": "application/json"
        }


def registrar_usuario(request):
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                if response.status_code == requests.codes.ok:
                    usuario = response.json()
                    user = User.objects.create_user(
                        username=formulario.cleaned_data.get("username"),
                        password=formulario.cleaned_data.get("password1"),
                        email=formulario.cleaned_data.get("email")
                    )
                    user.save()
                    user = authenticate(request, username=formulario.cleaned_data.get("username"), password=formulario.cleaned_data.get("password1"))
                    if user is not None:
                        auth_login(request, user)
                        token_acceso = obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                        )
                        request.session["usuario"] = usuario
                        request.session["token"] = token_acceso
                        return redirect("index")
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])
                    return render(request, 'registration/signup.html', {"formulario": formulario})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

def login(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data.get("usuario")
            password = formulario.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                token_acceso = obtener_token_session(username, password)
                request.session["token"] = token_acceso
                return redirect("index")
            else:
                formulario.add_error(None, "Credenciales inválidas")
    else:
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})


def obtener_token_session(usuario, password):
    token_url = 'http://127.0.0.1:8000/oauth2/token/'
    data = {
        'grant_type': 'password',
        'username': usuario,
        'password': password,
        'client_id': 'admin',
        'client_secret': 'admin',
    }

    response = requests.post(token_url, data=data)
    try:
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description", "Error desconocido"))
    except ValueError as val_err:
        print(f'Error al decodificar la respuesta JSON: {val_err}')
        raise Exception("Error al decodificar la respuesta JSON")

def logout(request):
    if 'token' in request.session:
        del request.session['token']
    auth_logout(request)
    return redirect('index')
#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)