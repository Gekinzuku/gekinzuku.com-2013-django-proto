from django.conf.urls import patterns, include, url

urlpatterns = patterns('forum.views',
    url(r'^$', 'forum_home'),
    url(r'^(?P<BoardID>\d+)-(?P<BoardStr>[\w-]+)/$', 'forum_board'),
    url(r'^topic/(?P<TopicID>\d+)-(?P<TopicStr>[\w-]+)/$', 'forum_topic', {'Page': 0}),

    # Actions
    url(r'^(?P<BoardID>\d+)/post/$', 'forum_new_topic'),
    url(r'^topic/(?P<TopicID>\d+)/post/$', 'forum_new_post'),
    url(r'^topic/(?P<TopicID>\d+)/delete/$', 'forum_delete_topic'),
    url(r'^post/(?P<PostID>\d+)/delete/$', 'forum_delete_post'),
    url(r'^post/(?P<PostID>\d+)/edit/$', 'forum_edit_post'),
    
)
