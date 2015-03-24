from django.conf.urls import patterns, url

from musicvoting import views

urlpatterns = patterns('',
                       # ex: /
                       url(r'^$', views.index, name='index'),
                       # ex: /dbimport/
                       url(r'^import/$', views.dbimport, name='dbimport'),
                       # ex: /importstatus/
                       url(r'^importstatus/$', views.dbimport_status, name='dbimport_status'),
                       # ex: /importadddirectory/
                       url(r'^importadddirectory/$', views.dbimport_add_directory, name='dbimport_add_directory'),
                       # ex: /importmarkremove/
                       url(r'^importmarkremove/$', views.dbimport_mark_remove, name='dbimport_mark_remove'),
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
                       # ex: /shutdown/
                       url(r'^shutdown/$', views.shutdown, name='shutdown'),
                       # ex: /activevotes/
                       url(r'^activevotes/$', views.active_votes, name='active_votes'),
                       # ex: /votenext/
                       url(r'^votenext/$', views.vote_unvote_next, name='vote_unvote_next'),
                       )

