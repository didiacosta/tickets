from tickets.celery import app
from .serializers import FotoSerializer
from tickets.structures import Structure
from rest_framework.response import Response
from rest_framework.request import Request
#from celery import shared_task

@app.task
def uploadPhotoTask(foto):
	return foto.upload_file()