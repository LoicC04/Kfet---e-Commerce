from django.db import models

class Personne(models.Model):
        nom = models.CharField(max_length=200)
        panier = models.ForeignKey(Panier)

