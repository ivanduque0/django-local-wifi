from django.contrib import admin
from .models import interacciones, usuarios, horariospermitidos
# Register your models here.


class interaccionesadmin(admin.ModelAdmin):

    fieldsets = [
        ("Historico de actividad", {'fields': ['cedula','nombre','fecha','hora','razon', 'contrato']}),
    ]

class usuariosadmin(admin.ModelAdmin):

    fieldsets = [
        ("usuario", {'fields': ['cedula','nombre','id_usuario']}),
    ]

admin.site.register(usuarios,usuariosadmin)
admin.site.register(interacciones, interaccionesadmin)
admin.site.register(horariospermitidos)