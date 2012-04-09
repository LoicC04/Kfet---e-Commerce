from django.conf.urls.defaults import patterns

urlpatterns = patterns('Kfet.Administration.views',

    # Index
    (r'^$', 'index'),

    # Gestion des menus
    (r'^typeMenu/$', 'typeMenu'),
    (r'^typeMenu/(?P<erreur>\d+)/$', 'typeMenu'),
    (r'^typeMenu/ajouter/$', 'ajouterModifierMenu'),
    (r'^typeMenu/modifier/(?P<menu_id>\d+)/$', 'ajouterModifierMenu'),
    (r'^typeMenu/supprimer/(?P<menu_id>\d+)/$', 'supprimerMenu'),

    # Gestion des types de paiement
    (r'^typePaiement/$', 'typePaiement'),

    # Gestion des dettes
    (r'^dettes/$', 'dettes'),
    #(r'^(?P<poll_id>\d+)/$', 'detail'),
)
