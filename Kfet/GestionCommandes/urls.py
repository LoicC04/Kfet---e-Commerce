from django.conf.urls.defaults import patterns

urlpatterns = patterns('Kfet.GestionCommandes.views',

    # Index
    (r'^$', 'index'),

    # ....
    (r'^list_commande/$', 'listCommande'),
    (r'^list_commande/(?P<statut>-?\d+)/$', 'listCommande'),
    (r'^majStatut/(?P<num_commande>\d+)/$', 'changerEtatCommande'),
    (r'^annuler/(?P<num_commande>\d+)/$', 'annuler'),

)
