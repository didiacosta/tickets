from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, Foto
from tickets.celery import app

class UserAppSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=User
		fields=('id','username')

class TicketSerializer(serializers.HyperlinkedModelSerializer):
	user = UserAppSerializer(read_only=True) 
	# user_id = serializers.PrimaryKeyRelatedField(write_only=True,
	# 	queryset=User.objects.all())
	porcentajeCumpletado = serializers.SerializerMethodField('_porcentaje',read_only=True)

	class Meta:
		model=Ticket
		fields=('id','user','fechaCreacion','cantidadFotos','completado','porcentajeCumpletado')

	def _porcentaje(self,obj):
		return str((Foto.objects.filter(ticket__id=obj.id).count()/obj.cantidadFotos)*100) + '%'

class TicketLiteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Ticket
		fields=('id',)

class FotoSerializer(serializers.HyperlinkedModelSerializer):
	ticket = TicketLiteSerializer(read_only=True) 
	ticket_id = serializers.PrimaryKeyRelatedField(write_only=True,
		queryset=Ticket.objects.all())
	foto_url = serializers.SerializerMethodField('_fotourl',read_only=True)

	class Meta:
		model=Foto
		fields=('id','ticket','ticket_id','foto_url','foto','fechaCreacion')

	def _fotourl(self,obj):
		return obj.foto.url

	@app.task
	def save(ticket_id,foto):
		obj=Foto.objects.create(ticket_id=ticket_id,foto=foto)
		obj.save()
		return obj
