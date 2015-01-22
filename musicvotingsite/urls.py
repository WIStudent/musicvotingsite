from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'musicvotingsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('musicvoting.urls', namespace='musicvoting')),
    url(r'^admin/', include(admin.site.urls)),
)
