from django.db import models
from Produit import Produit
from Categorie import Categorie
from TypeMenu import TypeMenu
from django import forms
from django.contrib.auth.models import User


class Menu(models.Model):
    typeMenu = models.ForeignKey(TypeMenu, blank=False, null=False)
    user = models.ForeignKey(User, blank=False, null=False)
    boisson = models.ForeignKey(Produit, blank=False, null=False, related_name="menu_boisson")
    plat = models.ForeignKey(Produit, blank=False, null=False, related_name="menu_plat")
    produit1 = models.ForeignKey(Produit, blank=False, null=False, related_name="menu_produit1")
    produit2 = models.ForeignKey(Produit, blank=True, null=True, related_name="menu_produit2")
    
    class Meta:
        app_label = 'Commun'

    def __unicode__(self):
       return "Menu {0} de {1}".format(self.typeMenu.nom, self.user.username);

class ChoisirMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude=('typeMenu', 'user')

    cat_boisson = Categorie.objects.filter(nom="Boisson")
    cat_plat = Categorie.objects.filter(nom="Pizza")
    cat_article = Categorie.objects.all().exclude(nom__in=["Pizza","Boisson"])

    boisson = forms.ModelChoiceField(Produit.objects.filter(categorie=cat_boisson))
    plat = forms.ModelChoiceField(Produit.objects.filter(categorie=cat_plat))
    produit1 = forms.ModelChoiceField(Produit.objects.filter(categorie__in=cat_article))
    produit2 = forms.ModelChoiceField(Produit.objects.filter(categorie__in=cat_article))
