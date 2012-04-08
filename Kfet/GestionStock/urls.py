from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Kfet.GestionStock.views',

    # index
    (r'^$', 'index'),
    (r'^reapprovisionnement/', 'reappro'),

    # Fournisseur
    (r'^creerFournisseur/$', 'creerFournisseur'),
    (r'^editerFournisseur/(?P<id>\d+)/$', 'creerFournisseur'),

    # Faire une commande
    (r'^commander/(?P<fournisseur_id>\d+)/$', 'commander'),
    (r'^commander/(?P<fournisseur_id>\d+)/(?P<erreur>\d+)/$', 'commander'),
    (r'^commande/(?P<produit_id>\d+)/$', 'commande'),
    (r'^validerCommande/(?P<fournisseur_id>\d+)/$', 'validerCommande'),
    
    # Produit 
    (r'^creerProduit/(?P<fournisseur_id>\d+)/$', 'creerProduit'),
    (r'^editerProduit/(?P<fournisseur_id>\d+)/(?P<produit_id>\d+)/$', 'creerProduit'),
    (r'^supprimerProduit/(?P<fournisseur_id>\d+)/(?P<produit_id>\d+)/$', 'supprimerProduit'),
    
    # Categorie
    (r'^creerCategorie/(?P<model_name>[a-zA-Z]+)/$', 'add_new_model'),
    (r'^creerTypeproduit/(?P<model_name>[a-zA-Z]+)/$', 'add_new_model'),

    #(r'^(?P<poll_id>\d+)/$', 'detail'),
)
