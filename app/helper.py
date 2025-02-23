import requests
import environ
import os
from pathlib import Path

# Cargar las variables de entorno desde el archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

class Helper:
    
    @staticmethod
    def obtener_url():
        """Devuelve la URL base de la API."""
        return "http://127.0.0.1:8000/api/v1/"
    
    @staticmethod
    def crear_cabecera():
        """Crea la cabecera con el token de autorización."""
        return {
            'Authorization': f'Bearer {env("TOKEN_ACCESO")}',
            "Content-Type": "application/json"
        }
    
    @staticmethod
    def procesar_respuesta(response):
        """Procesa la respuesta de la API y la convierte en JSON."""
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return response.json()
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            import xml.etree.ElementTree as ET
            return ET.fromstring(response.text)
        else:
            return response.text

    @staticmethod
    def obtener_cines():
        """Obtiene la lista de cines de la API."""
        headers = Helper.crear_cabecera()
        url = Helper.obtener_url() + 'cines'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener cines:", response.status_code)
            return []

    @staticmethod
    def obtener_empleados():
        """Obtiene la lista de empleados de la API."""
        headers = Helper.crear_cabecera()
        url = Helper.obtener_url() + 'empleados'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener empleados:", response.status_code)
            return []

    @staticmethod
    def obtener_salas():
        """Obtiene la lista de salas de la API."""
        headers = Helper.crear_cabecera()
        url = Helper.obtener_url() + 'salas'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener salas:", response.status_code)
            return []

    @staticmethod
    def obtener_sala(sala_id):
        """Obtiene una sala específica por ID."""
        headers = Helper.crear_cabecera()
        url = Helper.obtener_url() + f'salas/{sala_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener la sala:", response.status_code)
            return None

    @staticmethod
    def obtener_pelicula(pelicula_id):
        """Obtiene una película específica por ID."""
        headers = Helper.crear_cabecera()
        url = Helper.obtener_url() + f'peliculas/{pelicula_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener la película:", response.status_code)
            return None
