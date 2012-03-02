from django.db import models

# Create your models here.

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.FloatField(blank=True, null=True)

