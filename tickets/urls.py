from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from ticket.views import TicketViewSet, FotoViewSet


admin.autodiscover()
router =  routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'fotos', FotoViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'tickets.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include(router.urls)),
	url(r'^ticket/', include('ticket.urls')),
]
