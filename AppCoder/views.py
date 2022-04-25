from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse
from AppCoder.models import Libro, Autor, Genero, Avatar
from AppCoder.forms import LibroFormulario, AutorFormulario, GeneroFormulario, UserRegisterForm, UserEditForm, AvatarFormulario
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.http.request import QueryDict
#Para el login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def inicio(request):
    
    avatares = Avatar.objects.filter(user=request.user.id)
    
    return render(request, "AppCoder/inicio.html", {"url":avatares[0].imagen.url})

def libros(request):
    
    libros = Libro.objects.all()

    contexto= {"libros":libros} 

    return render(request, "AppCoder/libros.html", contexto)
      

def autores(request):
    autores = Autor.objects.all()

    contexto= {"autores":autores} 

    return render(request, "AppCoder/autores.html",contexto)

def generos(request):
    generos = Genero.objects.all()

    contexto= {"generos":generos} 

    return render(request, "AppCoder/generos.html",contexto)

def libroFormulario(request):
    if request.method == "POST":
        miFormulario = LibroFormulario(request.POST)
        print(miFormulario)
        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data
            libro = Libro (titulo=informacion["titulo"], autor=informacion["autor"], genero=informacion["genero"], fecha=informacion["fecha"])
            libro.save()
            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = LibroFormulario
    return render(request, "AppCoder/libroFormulario.html", {"miFormulario":miFormulario})

def autorFormulario(request):
    if request.method == "POST":
        miFormulario = AutorFormulario(request.POST)
        print(miFormulario)
        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data
            autor = Autor (nombre=informacion["nombre"], apellido=informacion["apellido"], genero=informacion["genero"])
            autor.save()
            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = AutorFormulario
    return render(request, "AppCoder/autorFormulario.html", {"miFormulario":miFormulario})

def generoFormulario(request):
    if request.method == "POST":
        miFormulario = GeneroFormulario(request.POST)
        print(miFormulario)
        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data
            genero = Genero (nombre=informacion["nombre"], descripcion=informacion["descripcion"])
            genero.save()
            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = GeneroFormulario
    return render(request, "AppCoder/generoFormulario.html", {"miFormulario":miFormulario})

def buscar(request):

      if  request.GET['titulo']:
            titulo = request.GET['titulo'] 
            libros = Libro.objects.filter(titulo__icontains=titulo)

            return render(request, "AppCoder/inicio.html", {"libros":libros, "titulo":titulo})

      else: 

            respuesta = 'No se encontraron resultados'
      return HttpResponse(respuesta)


def busquedaLibro(request):
     return render(request, "AppCoder/busquedaLibro.html")

def login_request(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():  # Si pasó la validación de Django

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username= usuario, password=contrasenia)

            if user is not None:
                login(request, user)

                return render(request, "AppCoder/inicio.html", {"mensaje":f"Bienvenido {usuario}"})

            else:
                return render(request, "AppCoder/inicio.html", {"mensaje":"Datos incorrectos"})
           
        else:

            return render(request, "AppCoder/inicio.html", {"mensaje":"Formulario erroneo"})

    form = AuthenticationForm()

    return render(request, "AppCoder/login.html", {"form": form})


def register(request):

      if request.method == 'POST':

            form = UserCreationForm(request.POST)
            form = UserRegisterForm(request.POST)
            if form.is_valid():

                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Usuario Creado :)"})

      else:
            form = UserCreationForm()       
            form = UserRegisterForm()     

      return render(request,"AppCoder/registro.html" ,  {"form":form})




@login_required
def editarPerfil(request):
      usuario = request.user
      if request.method == 'POST':
            miFormulario = UserEditForm(request.POST)
            if miFormulario.is_valid():
                  informacion = miFormulario.cleaned_data
            
                  usuario.email = informacion['email']
                  usuario.password1 = informacion['password1']
                  usuario.password2 = informacion['password2']
                  usuario.last_name = informacion['last_name']
                  usuario.first_name = informacion['first_name']
                  usuario.save()
                  return render(request, "AppCoder/inicio.html")
            
      else:
            miFormulario = UserEditForm(initial={'email': usuario.email})
      
      return render(request, "AppCoder/editarPerfil.html", {"miFormulario": miFormulario, "usuario": usuario})

def leerLibros(request):

      libros = Libro.objects.all()

      contexto= {"libros":libros} 

      return render(request, "AppCoder/libros.html",contexto)

def eliminarLibros(request, libro_titulo):
    libros = Libro.objects.get(titulo=libro_titulo)
    libros.delete()
    libros = Libro.objects.all()
    contexto = {"libros": libros}
    return render(request, "AppCoder/libros.html", contexto)

def editarLibro(request, libro_titulo):
  # Recibe el nombre del Libro que vamos a modificar
  libro = Libro.objects.get(titulo=libro_titulo)
  # Si es metodo POST hago lo mismo que el agregar
  if request.method == 'POST':
    # aquí me llega toda la información del html
    miFormulario = LibroFormulario(request.POST)
    print(miFormulario)
    if miFormulario.is_valid: # Si pasó la validación de Django
      informacion = miFormulario.cleaned_data
      libro.titulo = informacion['titulo']
      libro.autor = informacion['autor']
      libro.genero = informacion['genero']
      libro.fecha = informacion['fecha']
      libro.save()
      # Vuelvo al inicio o a donde quieran
      return render(request, "AppCoder/editarLibro.html")
  # En caso que no sea post
  else:
    # Creo el formulario con los datos que voy a modificar
    miFormulario = LibroFormulario(initial={'titulo': libro.titulo, 'autor': libro.autor,
                          'genero': libro.genero, 'fecha': libro.fecha})
  # Voy al html que me permite editar
  return render(request, "AppCoder/editarLibro.html", {"miFormulario": miFormulario, "libro_titulo": libro_titulo})

def leerGeneros(request):

      generos = Genero.objects.all()

      contexto= {"generos":generos} 

      return render(request, "AppCoder/generos.html",contexto)

def eliminarGeneros(request, genero_nombre):
    generos = Genero.objects.get(nombre=genero_nombre)
    generos.delete()
    generos = Genero.objects.all()
    contexto = {"generos": generos}
    return render(request, "AppCoder/generos.html", contexto)

def editarGenero(request, genero_nombre):
  # Recibe el nombre del Libro que vamos a modificar
  genero = Genero.objects.get(nombre=genero_nombre)
  # Si es metodo POST hago lo mismo que el agregar
  if request.method == 'POST':
    # aquí me llega toda la información del html
    miFormulario = GeneroFormulario(request.POST)
    print(miFormulario)
    if miFormulario.is_valid: # Si pasó la validación de Django
      informacion = miFormulario.cleaned_data
      genero.nombre = informacion['nombre']
      genero.descripcion = informacion['descripcion']
      genero.save()
      # Vuelvo al inicio o a donde quieran
      return render(request, "AppCoder/editarGenero.html")
  # En caso que no sea post
  else:
    # Creo el formulario con los datos que voy a modificar
    miFormulario = GeneroFormulario(initial={'nombre': genero.nombre, 'descripcion': genero.descripcion})
  # Voy al html que me permite editar
  return render(request, "AppCoder/editarGenero.html", {"miFormulario": miFormulario, "genero_nombre": genero_nombre})

@login_required
def agregarAvatar(request):
    if request.method == 'POST':
        miFormulario = AvatarFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            u = User.objects.get(username=request.user)
            avatar = Avatar(user=u,imagen=miFormulario.cleaned_data['imagen'])
            avatar.save()
            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario=AvatarFormulario()
    return render(request, "AppCoder/agregarAvatar.html", {"miFormulario":miFormulario})


def leerAutor(request):

      autores = Autor.objects.all()

      contexto= {"autores":autores} 

      return render(request, "AppCoder/autores.html",contexto)

def eliminarAutor(request, autor_nombre):
    autores = Autor.objects.get(nombre=autor_nombre)
    autores.delete()
    autores = Autor.objects.all()
    contexto = {"autores": autores}
    return render(request, "AppCoder/autores.html", contexto)

def editarAutor(request, autor_nombre):
  # Recibe el nombre del Libro que vamos a modificar
  autor = Autor.objects.get(nombre=autor_nombre)
  # Si es metodo POST hago lo mismo que el agregar
  if request.method == 'POST':
    # aquí me llega toda la información del html
    miFormulario = AutorFormulario(request.POST)
    print(miFormulario)
    if miFormulario.is_valid: # Si pasó la validación de Django
      informacion = miFormulario.cleaned_data
      autor.nombre = informacion['nombre']
      autor.apellido = informacion['apellido']
      autor.genero = informacion['genero']
      autor.save()
      # Vuelvo al inicio o a donde quieran
      return render(request, "AppCoder/inicio.html")
  # En caso que no sea post
  else:
    # Creo el formulario con los datos que voy a modificar
    miFormulario = AutorFormulario(initial={'nombre': autor.nombre, 'apellido': autor.apellido,
                          'genero': autor.genero})
  # Voy al html que me permite editar
  return render(request, "AppCoder/editarAutor.html", {"miFormulario": miFormulario, "autor_nombre": autor_nombre})


class AutorList(ListView):
    model = Autor
    template_name = "AppCoder/autor_list.html"

class AutorDetalle(DetailView):
    model = Autor
    template_name = "AppCoder/autor_detalle.html"

class AutorCreacion(CreateView):
    model = Autor
    success_url = "/AppCoder/autor/list"
    fields = ['nombre', 'apellido','genero']

class AutorUpdate(UpdateView):
    model = Autor
    success_url = "/AppCoder/autor/list"
    fields = ['nombre', 'apellido','genero']

class AutorDelete(DeleteView):
    model = Autor
    success_url = "/AppCoder/autor/list"