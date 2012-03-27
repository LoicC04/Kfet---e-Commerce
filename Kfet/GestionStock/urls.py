from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Kfet.GestionStock.views',
    (r'^$', 'index'),
    (r'^reapprovisionnement/', 'reappro'),
    (r'^creerFournisseur/$', 'creerFournisseur'),
    (r'^editerFournisseur/(?P<id>\d+)/$', 'creerFournisseur'),
    (r'^commander/(?P<fournisseur_id>\d+)/$', 'commander'),
    (r'^creerProduit/(?P<fournisseur_id>\d+)/$', 'creerProduit'),
    (r'^editerProduit/(?P<fournisseur_id>\d+)/(?P<produit_id>\d+)/$', 'creerProduit'),
    (r'^supprimerProduit/(?P<fournisseur_id>\d+)/(?P<produit_id>\d+)/$', 'supprimerProduit'),
    (r'^creerCategorie/(?P<model_name>[a-zA-Z]+)/$', 'add_new_model'),
    (r'^editerCategorie/(?P<categorie_id>\d+)/$', 'editerCategorie'),
    #(r'^(?P<poll_id>\d+)/$', 'detail'),
)
