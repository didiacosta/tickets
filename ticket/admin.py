from django.contrib import admin
from .models import Ticket,Foto


class AdminTicket(admin.ModelAdmin):
	list_display=('id','user','cantidadFotos','completado')
	search_fields=('id',)
	list_filter=('user','completado')


class AdminFoto(admin.ModelAdmin):
	list_display=('fechaCreacion','ticket','archivo')
	list_filter=('ticket',)

admin.site.register(Ticket,AdminTicket)
admin.site.register(Foto,AdminFoto)