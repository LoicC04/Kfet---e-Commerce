from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Commandes.views',

    #url(r'^$', 'home'),
    #(r'^$', 'index'),
    url(r'^panier_ajout/$', 'panier_ajout'), 
    url(r'^panier_suppr/(?P<produit_panier_id>\d+)/$', 'panier_suppr'), 
    url(r'^panier_maj/(?P<produit_panier_id>\d+)/$', 'panier_maj'),  
    url(r'^(?P<produit_id>\d+)/(?P<erreur>\d+)/$', 'produit'),
    url(r'^(?P<produit_id>\d+)/$', 'produit'),
    url(r'^panier/$', 'panier'),
    url(r'^categorie/(?P<cat_id>\d+)/$', 'categorie'),
    url(r'^validerPanier/$', 'validerPanier'),
    url(r'^choisirMenu/(?P<typeMenu_id>\d+)/$', 'choisirMenu'),
    #url(r'^choisirMenu/(?P<typeMenu_id>\d+)/(?P<menu_id>\d+)/$', 'Kfet.views.choisirMenu'),
)
