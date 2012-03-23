from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Kfet.GestionStock.views',
    (r'^$', 'index'),
    (r'^reapprovisionnement/', 'reappro'),
    (r'^creerFournisseur/', 'creerFournisseur'),
    #(r'^(?P<poll_id>\d+)/$', 'detail'),
)
