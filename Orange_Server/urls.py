from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Orange_Server.views import get_melon_chart
from Orange_Server.views import get_billboard_chart
from Orange_Server.views import get_oricon_chart
from Orange_Server.views import get_music_video_information
from Orange_Server.views import search_music_video_information
from Orange_Server.views import search_music_video_information_for_page

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Orange_Server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^getMelonChart', get_melon_chart),
    url(r'^getMusicVideoInformation', get_music_video_information),
    url(r'^searchMusicVideoInformationForPage', search_music_video_information_for_page),
    url(r'^searchMusicVideoInformation', search_music_video_information),
    url(r'^getBillboardChart', get_billboard_chart),
    url(r'^getOriconChart', get_oricon_chart),
)

urlpatterns += staticfiles_urlpatterns()
