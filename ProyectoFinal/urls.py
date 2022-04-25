from django.urls import path
from AppCoder import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('admin/', admin.site.urls),
    path('libros',views.libros, name="Libros"),
    path('autores', views.autores, name='Autores'),
    path('genero', views.generos, name="Géneros"),
    path('busquedaLibro', views.busquedaLibro, name="BusquedaLibro"),
    path('buscar/', views.buscar),
    path('libroFormulario', views.libroFormulario, name="LibroFormulario"),
    path('autorFormulario', views.autorFormulario, name="AutorFormulario"),
    path('generoFormulario', views.generoFormulario, name="GeneroFormulario"),
    path('login', views.login_request, name="Login"),
    path('register', views.register, name='Register'),
    path('logout', LogoutView.as_view(template_name='AppCoder/logout.html'), name='Logout'),
    path('leerLibros', views.leerLibros, name = "LeerLibros"),
    path('eliminarLibro/<libro_titulo>/', views.eliminarLibros, name="EliminarLibro"),
    path('editarLibro/<libro_titulo>/', views.editarLibro, name="EditarLibro"),
    path('autor/list', views.AutorList.as_view(), name='List'),
    path(r'^(?P<pk>\d+)$', views.AutorDetalle.as_view(), name='Detail'),
    path(r'^nuevo$', views.AutorCreacion.as_view(), name='New'),
    path(r'^editar/(?P<pk>\d+)$', views.AutorUpdate.as_view(), name='Edit'),
    path(r'^borrar/(?P<pk>\d+)$', views.AutorDelete.as_view(), name='Delete'),
    path('editarPerfil', views.editarPerfil, name="EditarPerfil"),
    path('agregarAvatar', views.agregarAvatar, name="AgregarAvatar"),
    path('eliminarGenero/<genero_nombre>/', views.eliminarGeneros, name="EliminarGenero"),
    path('leerGeneros', views.leerGeneros, name = "LeerGeneros"),
    path('editarGenero/<genero_nombre>/', views.editarGenero, name="EditarGenero"),
    path('eliminarAutor/<autor_nombre>/', views.eliminarAutor, name="EliminarAutor"),
    path('leerAutores', views.leerAutor, name = "LeerAutor"),
    path('editarAutores/<autor_nombre>/', views.editarAutor, name="EditarAutor"),
    ]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)