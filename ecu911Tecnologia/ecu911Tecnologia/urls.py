from django.conf.urls import patterns, include, url
from checklist.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ecu911Tecnologia.views.home', name='home'),
    # url(r'^ecu911Tecnologia/', include('ecu911Tecnologia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^tareas/$', tareas),
    url(r'^tareaEspecifica/$', tareaEspecifica),
    url(r'^calendario/$', calendario),
    url(r'guardarTareaEspecifica/$', guardarTareaEspecifica),
    url(r'validarDiaConUsuario/$', validarDiaConUsuario),

    url(r'^reporte/$', reporte),

    url(r'^obtenerMalas/$', obtenerMalas),
    url(r'^obtenerBuenas/$', obtenerBuenas),

    url(r'^mostrarMalas/$', mostrarMalas),
    url(r'^mostrarBuenas/$', mostrarBuenas),
)
handler404 = 'checklist.views.handler404'
