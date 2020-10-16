from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ValidationError, ModelForm
from .models import User, UserProfile
import random
import hashlib


class ChangeWidgetMixin:
    """Mixin for change widgets attributes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = ''


class LoginForm(ChangeWidgetMixin, AuthenticationForm):
    """Form for user login"""

    class Meta:
        model = User
        fields = ('username', 'password')


class UserForm(ChangeWidgetMixin, UserCreationForm):
    """Form class for user creation"""

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'age', 'email', 'avatar')

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise ValidationError(_('You are very young!'))
        return age

    def save(self):
        user = super().save()
        user.is_active = False
        salt = hashlib.sha1(
            str(random.random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user


class UserChangeForm(ChangeWidgetMixin, UserChangeForm):
    """Form class for updaiting user data"""

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'age', 'email', 'avatar')

    def clean_age(self):
        return UserForm.clean_age(self)


class UserProfileUpdateForm(ChangeWidgetMixin, ModelForm):
    """Form class for updating userprofile data"""

    class Meta:
        model = UserProfile
        fields = ('gender', 'tag', 'about')
