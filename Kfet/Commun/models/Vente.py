from django.db import models
from Produit import *


class Vente(models.Model):
        produit = models.ForeignKey(Produit)
        date = models.DateTimeField('date vente')
        quantite = models.IntegerField()

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return self.produit;
