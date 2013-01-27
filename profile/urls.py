from django.conf.urls import patterns, include, url

urlpatterns = patterns('profile.views',
    url(r'^$', 'profile_page', {'Username': None}),
    url(r'^activate/(?P<Key>\w+)/$', 'profile_activate'),
    url(r'^edit/', 'profile_edit'),
    url(r'^(?P<Username>\w+)/$', 'profile_page'),
    url(r'^(?P<Username>\w+)/achievements/$', 'achievements_page'),
)
