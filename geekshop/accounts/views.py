from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import SingleObjectMixin, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

from .models import User
from .forms import UserForm, UserChangeForm, UserProfileUpdateForm, LoginForm
from .utils import send_message


# Create your views here.

class UserLogin(UserPassesTestMixin, LoginView):
    """Class for user login"""

    success_url = reverse_lazy('mainapp:main')
    form_class = LoginForm

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.success_url)


class UserLogout(LogoutView):
    """Class for user logout"""

    success_message = _('You are logged out!')

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page:
            messages.success(self.request, self.success_message)
        return next_page


class UserCreateView(CreateView):
    """Class create new user in db"""

    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse_lazy('accounts:confirm')

    def form_valid(self, form):
        response = super().form_valid(form)
        if send_message(self.object):
            messages.success(self.request, _(
                'Activation message was sent succefully!'))
        else:
            messages.error(self.request, _(
                'Activation message was not sent. \
                Please, contact with administrator.'))
        return response


class RegistrationConfirm(TemplateView):
    """Class for information user about registration"""

    template_name = 'accounts/registration_confirm.html'


class VerifyEmail(SingleObjectMixin, TemplateView):
    """Class for activation user by activation key"""

    model = User
    template_name = 'accounts/verify_email.html'

    def get_object(self):
        username = self.kwargs.get('username')
        obj = get_object_or_404(self.model, username=username)
        return obj

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        return super().get_context_data(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        key = self.kwargs.get('key')
        if not self.object.is_active:
            if key == self.object.activation_key and \
                    self.object.is_activation_key_not_expired:
                self.object.is_active = True
                # self.object.activation_key = ''
                self.object.save()
                messages.success(self.request, _('confirmed'))
            else:
                if self.object.reset_activation_key():
                    messages.warning(self.request, _(
                        'Activation message was resent succefully!'))
                else:
                    messages.error(self.request, _('Activation message was not sent. \
                    Please, contact with administrator.'))
        else:
            messages.info(self.request, _('User is already activated!'))

        return response


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Class for updating user and userprofile data"""

    form_class = UserChangeForm
    template_name_suffix = '_update'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'profile_form': UserProfileUpdateForm(
            instance=self.object.userprofile)})
        return context

    def form_valid(self, form):
        with transaction.atomic():
            profile_form = UserProfileUpdateForm(
                self.request.POST, instance=self.object.userprofile)
            if profile_form.is_valid():
                return super().form_valid(form)
