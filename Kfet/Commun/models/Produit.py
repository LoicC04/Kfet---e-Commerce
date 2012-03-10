from django.db import models

from Menu import *
from Information import *
from Categorie import *	

class Produit(models.Model):
        nom = models.CharField(max_length=200)
        prix = models.FloatField(blank=True, null=True)
        menu = models.ForeignKey(Menu)
        info = models.ForeignKey(Information)
        categorie = models.ForeignKey(Categorie)

	class Meta:
            app_label = 'Commun'
