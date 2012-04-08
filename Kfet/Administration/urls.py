from django.conf.urls.defaults import patterns

urlpatterns = patterns('Kfet.Administration.views',
    (r'^$', 'index'),
    (r'^typeMenu/$', 'typeMenu'),
    (r'^typeMenu/ajouter/$', 'ajouterModifierMenu'),
    (r'^typeMenu/modifier/(?P<menu_id>\d+)/$', 'ajouterModifierMenu'),
    (r'^typePaiement/$', 'typePaiement'),
    (r'^dettes/$', 'dettes'),
    #(r'^(?P<poll_id>\d+)/$', 'detail'),
)
