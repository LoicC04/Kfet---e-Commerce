from django.db import models
from Produit import *
from django.contrib.auth.models import User


class Commentaire(models.Model):
        user = models.ForeignKey(User)
        commentaire = models.TextField()
        produit = models.ForeignKey(Produit)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return unicode(self.id);
