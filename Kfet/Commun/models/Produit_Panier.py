from django.db import models

class Produit_Panier(models.Model):
        quantite = models.IntegerField()
        produit = models.ForeignKey(Produit)
        panier = models.ForeignKey(Panier)
