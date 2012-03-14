from django.db import models
from Menu import *
from Categorie import *	
from Image import *

class Produit(models.Model):
        nom = models.CharField(max_length=200)
        prix = models.FloatField()
        menu = models.ForeignKey(Menu, blank=True, null=True)
        info = models.TextField()
        categorie = models.ForeignKey(Categorie)
        image = models.ForeignKey(Image)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
           return self.nom;
