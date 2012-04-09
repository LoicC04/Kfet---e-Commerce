from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('Kfet.Commandes.views',

    #Gestion commentaire
    url(r'^comm_suppr/(?P<comm_id>\d+)/$', 'comm_suppr'), 
    url(r'^comm_maj/(?P<comm_id>\d+)/$', 'comm_maj'),  

        
    #Gestion panier
    url(r'^panier_ajout/$', 'panier_ajout'), 
    url(r'^panier_suppr/(?P<produit_panier_id>\d+)/$', 'panier_suppr'), 
    url(r'^panier_menu_suppr/(?P<menu_id>\d+)/$', 'panier_menu_suppr'), 
    url(r'^panier_maj/(?P<produit_panier_id>\d+)/$', 'panier_maj'),  

    #Affichage produit
    url(r'^(?P<produit_id>\d+)/(?P<erreur>\d+)/$', 'produit'),
    url(r'^(?P<produit_id>\d+)/$', 'produit'),

    #Affichage panier
    url(r'^panier/$', 'panier'),
    url(r'^panier/(?P<erreur>\d+)$', 'panier'),

    #Affichage categorie
    url(r'^categorie/(?P<cat_id>\d+)/$', 'categorie'),

    #Validation panier
    url(r'^validerPanier/$', 'validerPanier'),
    url(r'^confirmationPanier/(?P<commande_id>\d+)/$', 'confirmationPanier'),

    #Menu
    url(r'^choisirMenu/(?P<typeMenu_id>\d+)/$', 'choisirMenu'),
    url(r'^choisirMenu/(?P<typeMenu_id>\d+)/(?P<menu_id>\d+)/$', 'choisirMenu'),
)
