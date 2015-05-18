# coding=utf-8
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from microsocial2.forms import BootstrapFormMixin
from users.models import User


class RegistrationForm(forms.ModelForm, BootstrapFormMixin):
    password1 = forms.CharField(label=_(u'пароль'), min_length=6, max_length=40, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_(u'повтор пароля'), min_length=6, max_length=40, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean(self):
        data = super(RegistrationForm, self).clean()
        if 'password1' not in self.errors and 'password2' not in self.errors:
            if data['password1'] != data['password2']:
                self.add_error('password1', ugettext(u'Пароли не совпадают.'))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(ugettext(u'Пользователь с таким email уже существует.'))
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.confirmed_registration = False
        if commit:
            user.save()
        return user
