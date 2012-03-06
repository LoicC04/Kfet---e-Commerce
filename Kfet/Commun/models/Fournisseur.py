from django.db import models

class Fournisseur(models.Model):
        nom = models.CharField(max_length=200)
        adresse = models.CharField(max_length=200)
        tel = models.CharField(max_length=10)
        mail = models.CharField(max_length=200)

