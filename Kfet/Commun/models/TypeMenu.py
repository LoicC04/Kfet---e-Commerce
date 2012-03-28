from django.db import models
from Produit import *
from django import forms

class TypeMenu(models.Model):
        nom = models.CharField(max_length=200)
        nombreArticles = models.IntegerField()
        prix = models.DecimalField(max_digits=10, decimal_places=2)
        description = models.TextField()

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return self.nom;

class CreationTypeMenuForm(forms.Form):
    class Meta:
        model = TypeMenu
