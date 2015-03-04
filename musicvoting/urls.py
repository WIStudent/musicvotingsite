from django.conf.urls import patterns, url

from musicvoting import views

urlpatterns = patterns('',
                       # ex: /
                       url(r'^$', views.index, name='index'),
                       # ex: /dbimport/
                       url(r'^dbimport/$', views.dbimport, name='dbimport'),
                       # ex: /artist/
                       url(r'^artist/$', views.artist, name='artist'),
                       # ex: /artist/2
                       url(r'^artist/(?P<pk>\d+)/$', views.artist_detail, name='artist_detail'),
                       # ex: /album/
                       url(r'^album/$', views.album, name='album'),
                       # ex: /album/2/
                       url(r'^album/(?P<pk>\d+)/$', views.album_detail, name='album_detail'),
                       # ex: /vote/2/
                       url(r'^vote/$', views.vote_track, name='vote_track'),
                       # ex: /unvote/2/
                       url(r'^unvote/$', views.unvote_track, name='unvote_track'),
                       # ex: /pause/
                       url(r'^pause/$', views.pause, name='pause'),
                       # ex: /unpause/
                       url(r'^unpause/$', views.unpause, name='unpause'),
                       # ex: /next/
                       url(r'^next/$', views.next_track, name='next'),
                       # ex: /search/
                       url(r'^search/$', views.search, name='search'),
                       # ex: /login/
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'musicvoting/login.html'}, name='login'),
                       # ex: /logout/
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       )

