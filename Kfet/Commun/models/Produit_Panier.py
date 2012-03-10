from django.db import models	

from Produit import *
from Panier import *

class Produit_Panier(models.Model):
        quantite = models.IntegerField()
        produit = models.ForeignKey(Produit)
        panier = models.ForeignKey(Panier)

	class Meta:
            app_label = 'Comm'
