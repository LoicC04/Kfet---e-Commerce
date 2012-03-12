from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('Kfet.Ventes.views',

    #url(r'^$', 'home'),
    #(r'^$', 'index'),
    url(r'^(?P<produit_id>\d+)/$', 'produit'),
    url(r'^categorie/(?P<cat_id>\d+)/$', 'categorie'),
)
