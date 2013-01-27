from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gekinzuku.views.home', name='home'),
    # url(r'^gekinzuku/', include('gekinzuku.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^profile/', include('profile.urls')),
    url(r'^forum/', include('forum.urls')),

    # I want the user login on root
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'profile.views.logout_page'),
    url(r'^register/$', 'profile.views.register_page'),

    url(r'^admin/', include(admin.site.urls)),
)
