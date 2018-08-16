# tickets

Proyecto desarrollado en Python 3.5
Los requerimientos del proyecto se encuentran relacionados en el requirements.txt

Endpoint para creacion de tickets (POST): http://localhost:8000/api/tickets/</br>
<b>usando los parametros en Headers:</b></br> Authorization: Token [token asociado al usuario]</br>
<b>usando los parametros en Body:</b></br> user_id, cantidadFotos

Endpoint para subir las imagenes(una a una)(POST): http://localhost:8000/ticket/</br>
<b>usando los parametros en Headers:</b></br> Authorization: Token [token asociado al usuario]</br>
<b>usando los parametros en Body:</b></br> foto, ticket_id
