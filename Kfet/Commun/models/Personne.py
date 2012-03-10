from django.db import models

from Panier import *

class Personne(models.Model):
        nom = models.CharField(max_length=200)
        panier = models.ForeignKey(Panier)

	class Meta:
            app_label = 'Commun'
