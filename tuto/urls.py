from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^polls/', include('tuto.polls.urls')),
    (r'^Stock/', 'tuto.Stock.views.index'),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
