from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Comptes.views',

    url(r'^creation/$', 'creation'),
    url(r'^ok/$', 'ok'),
#    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)
