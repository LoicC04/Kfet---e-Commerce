from django.db import models

from Produit import *

class Commentaire(models.Model):
        commentaire = models.TextField()
        produit = models.ForeignKey(Produit)

	class Meta:
            app_label = 'Commun'
