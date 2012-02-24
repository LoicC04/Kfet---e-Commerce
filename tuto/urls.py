from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^polls/$', 'tuto.polls.views.index'),
    (r'^polls/(?P<poll_id>\d+)/$', 'tuto.polls.views.detail'),
    (r'^polls/(?P<poll_id>\d+)/results/$', 'tuto.polls.views.results'),
    (r'^polls/(?P<poll_id>\d+)/vote/$', 'tuto.polls.views.vote'),
    (r'^admin/', include(admin.site.urls)),
)
