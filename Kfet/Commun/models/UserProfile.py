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

    dette = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        app_label = 'Commun'

def create_user_profile(sender, instance, promo, panier, created, dette=0, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, promo=promo, panier=panier, dette=0)

#post_save.connect(create_user_profile, sender=User)
