from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Kfet.Ventes.views',
    (r'^$', 'index'),
    #(r'^(?P<poll_id>\d+)/$', 'detail'),
)
