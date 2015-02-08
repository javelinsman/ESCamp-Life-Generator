from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'escamp_life.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^run/$', 'main.views.run'),
    url(r'^ref/$', 'main.views.ref'),
    url(r'^$', 'main.views.index'),
)
