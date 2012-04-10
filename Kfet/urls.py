from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'Kfet.views.home', name='home'),
    # url(r'^Kfet/', include('Kfet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^comptes/', include('Kfet.Comptes.urls')),
    (r'^ventes/', include('Kfet.Ventes.urls')),
    (r'^commandes/', include('Kfet.Commandes.urls')),
    (r'^gestionStock/', include('Kfet.GestionStock.urls')),
    (r'^administration/', include('Kfet.Administration.urls')),
    url(r'^$', 'Kfet.views.home'),
    url(r'^recherche/$', 'Kfet.views.recherche'),
    url(r'^menus/$', 'Kfet.views.listMenu'),

    
)

urlpatterns += staticfiles_urlpatterns()
