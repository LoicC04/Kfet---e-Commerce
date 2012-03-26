from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Comptes.views',

    url(r'^creation/$', 'creation'),
    url(r'^login/$', 'login'),
    url(r'^gestion/$', 'gestion'),  
#    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'comptes/login2.html'}),
    url(r'^ok/$', 'ok'),
)
