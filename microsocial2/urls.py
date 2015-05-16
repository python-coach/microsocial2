from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language
from microsocial2 import views


urlpatterns = [
    url(
        r'^$',
        views.main,
        name='main'
    ),
    url(
        r'^i18n/setlang/$',
        csrf_exempt(set_language),
        name='set_language'
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'', include('auths.urls')),
    url(r'', include('django.contrib.flatpages.urls')),
]
