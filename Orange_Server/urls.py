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
from Orange_Server.views import search_music_video_using_api
from Orange_Server.views import search_play_list
from Orange_Server.views import get_recent_play_list
from Orange_Server.views import get_play_list
from Orange_Server.views import get_high_cnt_play_list
from Orange_Server.views import upload_play_list
from Orange_Server.views import add_installed_count
from Orange_Server.views import get_installed_count
from Orange_Server.views import Test

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
    url(r'^searchPlayList', search_play_list),
    url(r'^getRecentPlayList', get_recent_play_list),
    url(r'^getPlayList', get_play_list),
    url(r'^getHighHitCountPlayList', get_high_cnt_play_list),
    url(r'^uploadPlayList', upload_play_list),
    url(r'^addInstalledCount', add_installed_count),
    url(r'^getInstalledCount', get_installed_count),
    url(r'^searchMusicVideoUsingApi', search_music_video_using_api),
    url(r'^test', Test),

)

urlpatterns += staticfiles_urlpatterns()
