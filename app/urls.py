from django.urls import path,re_path, include
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('clientes/listar',views.clientes_lista_api,name='cliente_lista'),
    path('salas/listar',views.salas_lista_api,name='sala_lista'),
    path('peliculas/listar',views.peliculas_lista_api,name='pelicula_lista'),
    path('cines/listar',views.cines_lista_api,name='cine_lista'),

    path('clientes/buscar',views.cliente_busqueda,name='cliente_buscar'),

    path('cines/buscar',views.cine_busqueda,name='cine_buscar'),
    #path('salas/buscar',views.sala_busqueda,name='sala_buscar'),
    #path('peliculas/buscar',views.pelicula_busqueda,name='pelicula_buscar'),
]