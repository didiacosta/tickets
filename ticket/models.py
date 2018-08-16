from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary.models import CloudinaryField

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class Ticket(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.PROTECT)
	cantidadFotos = models.IntegerField(default=1)
	completado = models.BooleanField(default=False)
	fechaCreacion = models.DateTimeField(auto_now_add=True)
	fechaActualizacion = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)

	def update(self, *args, **kwargs):
		super(Ticket, self).save(*args, **kwargs)
		nuevoEstado=None
		if self.cantidadFotos==Foto.objects.filter(ticket__id=self.id):
			nuevoEstado=True
		else:
			nuevoEstado=False
		if ~(nuevoEstado == self.completado):
			self.completado=nuevoEstado
			self.save() 


class Foto(models.Model):

	ticket= models.ForeignKey(Ticket,related_name="foto_ticket",on_delete=models.PROTECT)
	foto = CloudinaryField('image',null=True)
	fechaCreacion = models.DateTimeField(auto_now_add=True)


	def archivo(self):
		return """<a href="%s">archivo</a> """ % self.foto.url

	archivo.allow_tags = True

	def save(self, *args, **kwargs):
		super(Foto, self).save(*args, **kwargs)
		if self.ticket.cantidadFotos==Foto.objects.filter(ticket__id=self.ticket.id).count():
			self.ticket.completado=True
			self.ticket.save()

	def upload_file(self):
		print ('Cargando...')
		print (self.ticket)
		print (self.foto)
		f = Foto(
			ticket=self.ticket,
			foto=self.foto
			)
		f.save()
		return f.id


