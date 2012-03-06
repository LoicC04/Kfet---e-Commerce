from django.db import models

class Produit(models.Model):
        nom = models.CharField(max_length=200)
        prix = models.FloatField(blank=True, null=True)
        menu = models.ForeignKey(Menu)
        info = models.ForeignKey(Information)
        categorie = models.ForeignKey(Categorie)

