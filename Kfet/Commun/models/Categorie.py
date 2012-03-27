# -*- coding: utf-8 -*- 
from django.db import models
from django import forms


class Categorie(models.Model):
        nom = models.CharField(max_length=200)

        class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return self.nom;

class CreationCategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie

