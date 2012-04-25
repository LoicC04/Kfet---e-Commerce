from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Ventes.views',

    url(r'^(?P<promo_id>\d+)/(?P<open>\d+)/$', 'index'),
    url(r'^(?P<promo_id>\d+)/(?P<open>\d+)/(?P<erreur>\d+)/$', 'index'), 
    url(r'^produit_vente/(?P<produit_id>\d+)/$', 'produit_vente'),
    url(r'^annuler_vente/(?P<vente_id>\d+)/$', 'annuler_vente'), 
)
