from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    quantite = models.IntegerField()

    def __unicode__(self):
       return self.nom;
