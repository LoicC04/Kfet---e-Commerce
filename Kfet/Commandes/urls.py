from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Commandes.views',

    #url(r'^$', 'home'),
    #(r'^$', 'index'),
    url(r'^panier_ajout/$', 'panier_ajout'),  
    url(r'^(?P<produit_id>\d+)/$', 'produit'),
    url(r'^panier/$', 'panier'),
    url(r'^categorie/(?P<cat_id>\d+)/$', 'categorie'),
    url(r'^validerPanier/$', 'validerPanier'),
)
