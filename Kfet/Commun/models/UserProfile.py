from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from Panier import *
from Promo import *


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    promo = models.ForeignKey(Promo, blank=True, null=True)
    panier = models.ForeignKey(Panier, blank=True, null=True)

    class Meta:
        app_label = 'Commun'

def create_user_profile(sender, instance, promo, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, promo=promo)

#post_save.connect(create_user_profile, sender=User)
