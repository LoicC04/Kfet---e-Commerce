from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Comptes.views',

    url(r'^creation/$', 'creation'),
    url(r'^ok/$', 'creation'),
)
