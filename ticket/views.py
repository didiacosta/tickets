from django.shortcuts import render, render_to_response
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, response
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse,JsonResponse
import datetime
from rest_framework.parsers import FormParser,MultiPartParser
#from django.contrib.auth.models import User

from tickets.functions import functions
from tickets.structures import Structure

#modelos
from .models import Ticket, Foto

#serializadores
from .serializers import UserAppSerializer, TicketSerializer, FotoSerializer

from .tasks import uploadPhotoTask

from rest_framework.authtoken.models import Token

class TicketViewSet(viewsets.ModelViewSet):
	"""
		Retorna una lista de tickets a los que tiene acceso, bajo la estructura 
		{'id','user','cantidadFotos','completado'}.<br/>
		Utilice el parametro <b>since</b> para obtener los tickets creados desde 
		una fecha especifica (YYYY-MM-DD).<br/>
		Utilice el parametro <b>until</b> para obtener los tickets creados hasta 
		una fecha especifica (YYYY-MM-DD).<br/>
		Utilice el parametro <b>full=[1|0]</b> para obtener los tickets completados (1) 
		o por completar (0).<br/>
		Utilice el parametro <b>id</b> para obtener el detalle un ticket especifico. 
		solo se podran consultar los tickets a los que tenga acceso el usuario actual.</br></br>

		<b>Restriccion: </b> Un usuario solo tendra acceso a los tickets que haya creado.


	"""
	model=Ticket
	queryset = model.objects.all()
	serializer_class = TicketSerializer
	module_name='tickets.ticket'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			if instance.user.id==request.user.id:
				serializer = self.get_serializer(instance)
				respuesta = Structure.success('' ,serializer.data)
				return Response(respuesta)
			else:
				respuesta = Structure.success('Lo sentimos, usted no tiene acceso al ticket especificado' ,None)
				return Response(respuesta)
		except Exception as e:
			functions.toLog(e,self.module_name)
			respuesta = Structure.success('Lo sentimos, no se encontraron datos' ,None)
			return Response(respuesta)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(TicketViewSet, self).get_queryset()
			user_id = request.user.id
			since = self.request.query_params.get('since', None)
			until = self.request.query_params.get('until', None)
			full = self.request.query_params.get('full', None)

			
			qset = (Q(user__id=user_id))
			if since:
				qset = qset & (Q(fechaCreacion__gte=datetime.datetime.strptime(since, "%Y-%m-%d").date()))
			if until:
				qset = qset & (Q(fechaCreacion__lte=datetime.datetime.strptime(until, "%Y-%m-%d").date()))
			if full:
				qset = qset & (Q(completado=full))

			queryset = self.model.objects.filter(qset)
			mensaje = 'No se encontraron registros con los criterios de busqueda ingresados.' if queryset.count()==0 else ''
			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = self.get_serializer(page,many=True)
				print(serializer)
				respuesta = Structure.success(mensaje ,serializer.data)
				return self.get_paginated_response(respuesta)

			serializer = self.get_serializer(queryset,many=True)
			respuesta = Structure.success(mensaje ,serializer.data)
			return Response(respuesta)

		except Exception as e:
			functions.toLog(e,self.module_name)
			respuesta = Structure.error500()
			return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


	@transaction.atomic
	def create(self, request, *args, **kwargs):
		
		if request.method == 'POST':
			sid = transaction.savepoint()
			try:
				serializer = TicketSerializer(data=request.POST,context={'request': request})
				if serializer.is_valid():
					serializer.save(user_id=Token.objects.get(key=request.auth).user_id)
					transaction.savepoint_commit(sid)
					respuesta = Structure.success('El registro se ha guardado correctamente' ,None)
					return Response(respuesta)
				else:
					errores=''
					transaction.savepoint_rollback(sid)
					print (serializer.errors)
					for x in serializer.errors:						
						errores= errores + serializer.errors[x][0]+'\n'					
						respuesta=Structure.error(errores)
						return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

			except Exception as e:
				transaction.savepoint_rollback(sid)
				functions.toLog(e,self.module_name)
				respuesta = Structure.error500()
				return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FotoViewSet(viewsets.ModelViewSet):

	model=Foto
	queryset = model.objects.all()
	serializer_class = FotoSerializer
	module_name='tickets.foto'
	parser_classes = (MultiPartParser,FormParser,)

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			if instance.ticket.user.id==request.user.id:
				serializer = self.get_serializer(instance)
				respuesta = Structure.success('' ,serializer.data)
				return Response(respuesta)
			else:
				respuesta = Structure.success('Lo sentimos, usted no tiene acceso al ticket especificado' ,None)
				return Response(respuesta)
		except Exception as e:
			functions.toLog(e,self.module_name)
			respuesta = Structure.success('Lo sentimos, no se encontraron datos' ,None)
			return Response(respuesta)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(FotoViewSet, self).get_queryset()
			ticket = self.request.query_params.get('ticket', None)
			user_id = request.user.id
			print ('ticket: ')
			print (ticket)
			qset = (Q(ticket__user__id=user_id))
			if ticket:
				qset = qset & (Q(ticket__id=ticket))

			queryset = self.model.objects.filter(qset)
			mensaje = 'No se encontraron registros con los criterios de busqueda ingresados.' if queryset.count()==0 else ''
			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = self.get_serializer(page,many=True)
				print(serializer)
				respuesta = Structure.success(mensaje ,serializer.data)
				return self.get_paginated_response(respuesta)

			serializer = self.get_serializer(queryset,many=True)
			respuesta = Structure.success(mensaje ,serializer.data)
			return Response(respuesta)

		except Exception as e:
			functions.toLog(e,self.module_name)
			respuesta = Structure.error500()
			return Response(respuesta)

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		#import pdb; pdb.set_trace()
		if request.method == 'POST':
			ticket=Ticket.objects.get(id=request.POST['ticket_id'])
			if ticket.completado:
				respuesta = Structure.success('No se puede subir la foto porque el ticket ya esta completo.' ,None)
				return Response(respuesta)				
			else:
				sid = transaction.savepoint()
				try:
					serializer = FotoSerializer(data=request.POST,context={'request': request})
					print (request.FILES)
					if serializer.is_valid():
						serializer.save(
							ticket_id=request.POST['ticket_id'],
							foto=request.FILES['foto']
						)
						transaction.savepoint_commit(sid)
						respuesta = Structure.success('El registro se ha guardado correctamente' ,None)
						return Response(respuesta)
					else:
						transaction.savepoint_rollback(sid)
						errores=''
						print (serializer.errors)
						for x in serializer.errors:						
							errores= errores + serializer.errors[x][0]+'\n'					
							respuesta=Structure.error(errores)
							return Response(respuesta)

				except Exception as e:
					transaction.savepoint_rollback(sid)
					functions.toLog(e,self.module_name)
					respuesta = Structure.error500()
					return Response(respuesta)

def uploadPhoto(request):
	print (request.META['HTTP_AUTHORIZATION'].split(' ')[1])
	token=Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1])
	if token:
		if request.method=='POST':
			try:
				f = Foto(
					ticket_id=request.POST['ticket_id'],
					foto=request.FILES['foto']
					)
				uploadPhotoTask.delay(f)
				respuesta = Structure.success('El registro se ha guardado correctamente,' + 
					'carga del archivo en progreso...' ,None)
				# return Response(respuesta)	
				return JsonResponse(respuesta)			
			except Exception as e:
				functions.toLog(e,'uploadPhoto')
				respuesta = Structure.error500()
				return Response(respuesta)
	else:
		return JsonResponse(Structure.error('Las credenciales de autenticacion no se proveyeron...'))
