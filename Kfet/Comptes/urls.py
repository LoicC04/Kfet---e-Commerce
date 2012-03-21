from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Comptes.views',

    url(r'^creation/(?P<erreur>\d+)$', 'creation'),
    url(r'^ajout/$', 'ajout'),
    url(r'^ok/$', 'ok'),
    url(r'^test/$', 'test'),

)
