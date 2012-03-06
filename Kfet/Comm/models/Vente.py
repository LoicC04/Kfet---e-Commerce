from django.db import models

from Produit import *
from Date import *

class Vente(models.Model):
        produit = models.ForeignKey(Produit)
        date = models.ForeignKey(Date)
        quantite = models.IntegerField()

	class Meta:
            app_label = 'Comm'
