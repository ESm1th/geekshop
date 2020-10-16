from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings

import random
import hashlib


def send_message(instance):
    user = instance
    verify_link = reverse_lazy('accounts:verify', args=[
                               user.username, user.activation_key])
    title = _('{} user account verification').format(user.username)
    message = _(
        'To confirm your account {} on portal \
         {} follow the link:\n \
         {}{}').format(user.username, settings.DOMAIN_NAME, settings.DOMAIN_NAME, verify_link )
    return send_mail(title, message, settings.EMAIL_HOST_USER,
                     [user.email], fail_silently=True)


def key_hasher(var):
    salt = hashlib.sha1(
        str(random.random()).encode('utf-8')).hexdigest()[:6]
    key = hashlib.sha1(
        (var + salt).encode('utf-8')).hexdigest()
    return key
