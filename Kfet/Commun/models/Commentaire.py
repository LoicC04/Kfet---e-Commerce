from django.db import models
from Produit import *
from UserProfile import *


class Commentaire(models.Model):
        profile = models.ForeignKey(UserProfile)
        commentaire = models.TextField()
        produit = models.ForeignKey(Produit)
        date = models.DateTimeField(auto_now_add = True, auto_now = True)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return unicode(self.id);
