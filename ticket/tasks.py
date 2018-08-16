from tickets.celery import app
from .serializers import FotoSerializer
from tickets.structures import Structure
from rest_framework.response import Response
from rest_framework.request import Request
from celery import shared_task

@shared_task
def uploadPhotoTask(foto):
	import pdb; pdb.set_trace()
	return foto.upload_file()