from django.contrib import admin
from .models import * 

#Importamos el archivo models
#Registramos los modelos
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Avatar)