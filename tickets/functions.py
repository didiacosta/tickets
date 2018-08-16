from datetime import *
import os
from django.conf import settings
import boto 
from boto.s3.key import Key
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import uuid
import sys,os
from log_errors.models import Excepciones

class functions:	

	@staticmethod
	def toLog(e,modulo):
		ahora=datetime.now()
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		exepciones = Excepciones();
		exepciones.error = ('\n'+ str(ahora) + '--> ' + str(fname) +
			' linea ' + str(exc_tb.tb_lineno) + ' --> ' + modulo + ': ' + str(e))
		exepciones.modulo = modulo
		exepciones.save()
		