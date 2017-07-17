from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Wechat_site(models.Model):
    name = models.CharField(max_length=50, blank=False)
    appid = models.CharField(max_length=18, blank=False)
    appsecret = models.CharField(max_length=32, blank=False)
    accesstoken = models.CharField(max_length=512, blank=True)
    expires_in = models.IntegerField(null=True, blank=True)
    gettokentime = models.DateTimeField(null=True, blank=True)
