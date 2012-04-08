from django.db import models
from Categorie import Categorie
from django import forms
from Kfet.widgets import SelectWithPopUp 


class TypeMenu(models.Model):
        nom = models.CharField(max_length=200)
        nombreArticles = models.IntegerField()
        categorie = models.ForeignKey(Categorie)
        prix = models.DecimalField(max_digits=10, decimal_places=2)
        description = models.TextField()

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return self.nom;

class TypeMenuForm(forms.ModelForm):
    class Meta:
        model = TypeMenu

    categorie = forms.ModelChoiceField(Categorie.objects, widget=SelectWithPopUp, label="Categorie du plat")
    nombreArticles = forms.IntegerField(label="Nombre d'articles", min_value=0)
