from django.db import models

class Categorie(models.Model):
        nom = models.CharField(max_length=200)
