from django.conf.urls import url
from auths import views


urlpatterns = [
    url(
        r'^login/$',
        views.login_view,
        name='login'
    ),
    url(
        r'^registraion/$',
        views.RegistrationView.as_view(),
        name='registraion'
    ),
    url(
        r'^password-recovery/$',
        views.PasswordRecoveryView.as_view(),
        name='password_recovery'
    ),
]
