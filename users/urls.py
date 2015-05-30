from django.conf.urls import url
from users import views


urlpatterns = [
    url(
        r'^profile/(?P<user_id>\d+)/$',
        views.UserProfileView.as_view(),
        name='user_profile'
    ),
    url(
        r'^settings/$',
        views.UserSettingsView.as_view(),
        name='user_settings'
    ),
]
