from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from Orange_Server.views import get_melon_chart

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Orange_Server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^getMelonChart', get_melon_chart)
)
