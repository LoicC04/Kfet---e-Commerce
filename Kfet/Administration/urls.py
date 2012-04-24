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
    (r'^typeMenu/activer/(?P<menu_id>\d+)/$', 'activerMenu'),

    # Gestion des types de paiement
    (r'^typeReglement/$', 'typeReglement'),
    (r'^typeReglement/(?P<erreur>\d+)/$', 'typeReglement'),
    (r'^typeReglement/ajouter/$', 'ajouterModifierReglement'),
    (r'^typeReglement/modifier/(?P<reglement_id>\d+)/$', 'ajouterModifierReglement'),
    (r'^typeReglement/supprimer/(?P<reglement_id>\d+)/$', 'supprimerReglement'),

    # Gestion des dettes
    (r'^dettes/$', 'dettes'),
    (r'^effacerDette/(?P<user_id>\d+)/$', 'effacerDette'),
    (r'^enleverDeDette/(?P<user_id>\d+)/$', 'enleverDeDette'),
    #(r'^(?P<poll_id>\d+)/$', 'detail'),

    # Gestion des dettes
    (r'^ventes/$', 'ventes'),

)
