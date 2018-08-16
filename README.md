# tickets

Proyecto desarrollado en Python 3.5
Los requerimientos del proyecto se encuentran relacionados en el requirements.txt

Endpoint para creacion de tickets (POST): http://localhost:8000/api/tickets/</br>
<b>usando los parametros en Headers:</b></br> Authorization: Token [token asociado al usuario]</br>
<b>usando los parametros en Body:</b></br> cantidadFotos [Numero]

Endpoint para subir las imagenes(una a una)(POST): http://localhost:8000/ticket/</br>
<b>usando los parametros en Headers:</b></br> Authorization: Token [token asociado al usuario]</br>
<b>usando los parametros en Body:</b></br> foto [Archivo], ticket_id [Numero]</br>
<i>Nota: </i> Utiliza Celery, por lo cual, es necesario levantar el celery: python35 manage.py celery worker -A tickets.celery --loglevel=info

Endpoint para ver los tickets a los que tiene acceso el usuario asociado al token entregado al servicio (GET): http://localhost:8000/api/tickets/</br>
<b>usando los parametros en Headers:</b></br> Authorization: Token [token asociado al usuario]</br>
<b>usando los parametros en url:</b></br> since [Fecha], until [Fecha], full [1|0]</br>
los parametros since (fecha desde), until (fecha hasta), full (1 ó 0) pueden combinarse para filtrar por rango de fechas[since --> until] y por estado (completado o no completado)

Endpoint para ver un ticket en especifico, solo si tiene acceso a él (GET): http://localhost:8000/api/tickets/[id del ticket]

