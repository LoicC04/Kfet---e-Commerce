from django.conf.urls.defaults import patterns

urlpatterns = patterns('Kfet.GestionCommandes.views',

    # Index
    (r'^$', 'index'),

    # ....
    (r'^list_commande/$', 'listCommande'),
    (r'^list_commande/(?P<statut>-?\d+)/$', 'listCommande'),

)
