from django.db import models
from Panier import *
from Promo import *


class Personne(models.Model):
        num_etu = models.CharField(max_length=9)
        nom = models.CharField(max_length=200)
        prenom = models.CharField(max_length=200)
        password = models.CharField(max_length=200)
        mail = models.CharField(max_length=200)
        promo = models.ForeignKey(Promo)
        panier = models.ForeignKey(Panier)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return self.nom;
