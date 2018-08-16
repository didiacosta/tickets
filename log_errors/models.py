from django.db import models

# Create your models here.

class Excepciones(models.Model):
	fecha_registro = models.DateTimeField(auto_now_add=True, blank=True)
	error = models.TextField(blank=True)
	modulo = models.CharField(blank=True, max_length=100)
	class Meta:				
		permissions = (
			("can_see_excepciones","can see excepciones"),
		)

	@staticmethod
	def toLog(e,modulo):
		ahora=datetime.now()
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		exepciones = Excepciones();
		exepciones.error = ('\n'+ str(ahora) + '--> ' + str(fname) +' linea ' + str(exc_tb.tb_lineno) + ' --> ' + modulo + ': ' + e.message)
		exepciones.modulo = modulo
		exepciones.save()