from django.db import models

class Vente(models.Model):
        produit = models.ForeignKey(Produit)
        date = models.ForeignKey(Date)
        quantite = models.IntegerField()

