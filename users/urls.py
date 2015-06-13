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
    url(
        r'^friends/$',
        views.UserFriendsView.as_view(),
        name='user_friends'
    ),
    url(
        r'^friends/incoming/$',
        views.UserIncomingView.as_view(),
        name='user_incoming'
    ),
    url(
        r'^friends/outcoming/$',
        views.UserOutcomingView.as_view(),
        name='user_outcoming'
    ),
    url(
        r'^api/friendship/$',
        views.FriendshipAPIView.as_view(),
        name='user_friendship_api'
    ),
    url(
        r'^search/$',
        views.SearchView.as_view(),
        name='user_search'
    ),
]
