from django.db import models

class Commentaire(models.Model):
        commentaire = models.TextField()
        produit = models.ForeignKey(Produit)

