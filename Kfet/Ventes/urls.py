from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Ventes.views',

    url(r'^$', 'index'), 
    url(r'^produit_vente/(?P<produit_id>\d+)/$', 'produit_vente'), 
)
