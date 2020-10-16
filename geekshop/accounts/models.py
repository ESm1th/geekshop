from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now, timedelta
from django.dispatch import receiver
from django.utils.functional import cached_property

from .utils import key_hasher, send_message

# Create your models here.


class User(AbstractUser):
    """Class represent user table in db"""

    # age = models.PositiveIntegerField(_('age'))
    age = models.PositiveIntegerField(_('age'), default=18)
    avatar = models.ImageField(
        _('avatar'), upload_to='media/images', max_length=250, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def is_activation_key_not_expired(self):
        return now() <= self.activation_key_expires

    def reset_activation_key(self):
        self.activation_key = key_hasher(self.email)
        self.activation_key_expires = now() + timedelta(hours=48)
        self.save()
        return send_message(self)

    def get_absolute_url(self):
        return reverse_lazy('mainapp:main')

    @cached_property
    def get_card(self):
        return self.basket.last()


class UserProfile(models.Model):
    """Class represent userprofile as one-to-one field to User model"""

    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    user = models.OneToOneField(
        User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    gender = models.CharField(
        _('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    tag = models.CharField(_('tags'), max_length=128, blank=True)
    about = models.TextField(_('about'), max_length=512, blank=True)

    @receiver(post_save, sender=User)
    def create_or_save_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        else:
            instance.userprofile.save()
