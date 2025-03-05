from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clientes/listar', views.clientes_lista_api, name='cliente_lista'),
    path('salas/listar', views.salas_lista_api, name='sala_lista'),
    path('peliculas/listar', views.peliculas_lista_api, name='pelicula_lista'),
    path('cines/listar', views.cines_lista_api, name='cine_lista'),

    path('clientes/buscar', views.cliente_busqueda, name='cliente_buscar'),

    path('cines/buscar', views.cine_busqueda, name='cine_buscar'),
    path('salas/buscar', views.sala_busqueda, name='sala_buscar'),
    path('peliculas/buscar', views.pelicula_busqueda, name='pelicula_busqueda'),

    path('clientes/post', views.cliente_post, name='cliente_post'),
    path('clientes/<int:cliente_id>/editar', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:cliente_id>/actualizar/nombre', views.cliente_editar_nombre, name='cliente_editar_nombre'),
    path('clientes/<int:cliente_id>/eliminar', views.cliente_eliminar, name='cliente_eliminar'),

    path('salas/create', views.sala_crear, name='sala_crear'),
    path('salas/<int:sala_id>/editar', views.sala_editar, name='sala_editar'),
    path('salas/<int:sala_id>/actualizar/tamano', views.sala_actualizar_tamano, name='sala_actualizar_tamano'),
    path('salas/<int:sala_id>/eliminar', views.sala_eliminar, name='sala_eliminar'),

    path('peliculas/create', views.pelicula_crear, name='pelicula_crear'),
    path('peliculas/<int:pelicula_id>/editar', views.pelicula_editar, name='pelicula_editar'),
    path('peliculas/<int:pelicula_id>/actualizar/nombre', views.pelicula_actualizar_nombre, name='pelicula_actualizar_nombre'),
    path('peliculas/<int:pelicula_id>/eliminar', views.pelicula_eliminar, name='pelicula_eliminar'),

    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
]