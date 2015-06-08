# coding=utf-8
from django.contrib import messages
from django.contrib.auth import BACKEND_SESSION_KEY, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, View
from users.forms import UserProfileForm, UserPasswordChangeForm, UserEmailChangeForm, UserWallPostForm
from django.utils.translation import ugettext as _
from users.models import User, FriendInvite


class UserProfileView(TemplateView):
    template_name = 'users/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.pk == int(kwargs['user_id']):
            self.user = request.user
        else:
            self.user = get_object_or_404(User, pk=kwargs['user_id'])
        self.wall_post_form = UserWallPostForm(request.POST or None)
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get_wall_posts(self):
        paginator = Paginator(self.user.wall_posts.select_related('author'), 20)
        page = self.request.GET.get('page')
        try:
            wall_posts = paginator.page(page)
        except PageNotAnInteger:
            wall_posts = paginator.page(1)
        except EmptyPage:
            wall_posts = paginator.page(paginator.num_pages)
        return wall_posts

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile_user'] = self.user
        context['wall_posts'] = self.get_wall_posts()
        context['wall_post_form'] = self.wall_post_form
        if self.request.user != self.user:
            context['is_my_friend'] = User.friendship.are_friends(self.request.user, self.user)
        return context

    def post(self, request, *args, **kwargs):
        if self.wall_post_form.is_valid():
            post = self.wall_post_form.save(commit=False)
            post.user = self.user
            post.author = request.user
            post.save()
            messages.success(request, _(u'Сообщение успешно опубликовано.'))
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class UserSettingsView(TemplateView):
    template_name = 'users/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        action = request.POST.get('action')
        self.profile_form = UserProfileForm(
            (request.POST if action == 'profile' else None),
            (request.FILES if action == 'profile' else None),
            prefix='profile', instance=request.user
        )
        self.password_form = UserPasswordChangeForm(request.user, (request.POST if action == 'password' else None),
                                                    prefix='password')
        self.email_form = UserEmailChangeForm(request.user, (request.POST if action == 'email' else None),
                                              prefix='email')
        return super(UserSettingsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserSettingsView, self).get_context_data(**kwargs)
        context['profile_form'] = self.profile_form
        context['password_form'] = self.password_form
        context['email_form'] = self.email_form
        return context

    def post(self, request, *args, **kwargs):
        if self.profile_form.is_valid():
            self.profile_form.save()
            messages.success(request, _(u'Профиль успешно сохранен.'))
            return redirect(request.path)
        elif self.password_form.is_valid():
            self.password_form.save()
            request.user.backend = request.session[BACKEND_SESSION_KEY]
            login(request, request.user)
            messages.success(request, _(u'Пароль успешно изменен.'))
            return redirect(request.path)
        elif self.email_form.is_valid():
            self.email_form.save()
            messages.success(request, _(u'Email успешно изменен.'))
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class UserFriendsView(TemplateView):
    template_name = 'users/friends_friends.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserFriendsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserFriendsView, self).get_context_data(**kwargs)
        context['friends_menu'] = 'friends'
        paginator = Paginator(self.request.user.friends.all(), 20)
        page = self.request.POST.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context


class UserIncomingView(TemplateView):
    template_name = 'users/friends_incoming.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserIncomingView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserIncomingView, self).get_context_data(**kwargs)
        context['friends_menu'] = 'incoming'
        paginator = Paginator(self.request.user.in_friend_invites.all(), 20)
        page = self.request.POST.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context


class UserOutcomingView(TemplateView):
    template_name = 'users/friends_outcoming.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserOutcomingView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserOutcomingView, self).get_context_data(**kwargs)
        context['friends_menu'] = 'outcoming'
        paginator = Paginator(self.request.user.out_friend_invites.all(), 20)
        page = self.request.POST.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context


class FriendshipAPIView(View):
    @method_decorator(login_required)
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        method_name = '_action_{}'.format(request.POST.get('action', ''))
        if not hasattr(self, method_name):
            raise Http404
        default_url = getattr(self, method_name)()
        return redirect(request.POST.get('next') or default_url or 'main')

    def _get_user_from_post_field(self, field_name):
        try:
            return User.objects.get(pk=self.request.POST.get(field_name))
        except (User.DoesNotExist, ValueError):
            pass

    def _action_add_to_friends(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            try:
                r = FriendInvite.objects.add(self.request.user, user)
            except ValueError, e:
                messages.warning(self.request, e)
            else:
                if r == 1:
                    messages.success(self.request, _(u'Заявка успешно отправлена и ожидает рассмотрения.'))
                elif r == 2:
                    messages.success(self.request, _(u'Пользователь успешно добавлен в друзья.'))
                    return 'user_friends'
        return 'user_outcoming'

    def _action_delete_from_friends(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            if User.friendship.delete(self.request.user, user):
                messages.success(self.request, _(u'Пользователь успешно удален из друзей.'))
        return 'user_friends'

    def _action_approve(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            try:
                r = FriendInvite.objects.approve(user, self.request.user)
            except ValueError, e:
                messages.warning(self.request, e)
            else:
                if r:
                    messages.success(self.request, _(u'Заявка успешно подтверждена. Пользователь добавлен в друзья.'))
        return 'user_incoming'

    def _action_reject(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            FriendInvite.objects.reject(user, self.request.user)
            messages.success(self.request, _(u'Заявка успешно отклонена.'))
        return 'user_incoming'

    def _action_cancel_outcoming(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            FriendInvite.objects.filter(from_user=self.request.user, to_user=user).delete()
            messages.success(self.request, _(u'Заявка успешно отменена.'))
        return 'user_incoming'
