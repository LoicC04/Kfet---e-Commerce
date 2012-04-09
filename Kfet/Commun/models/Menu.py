from django.db import models
from Produit import Produit
from Categorie import Categorie
from TypeMenu import TypeMenu
from Panier import Panier
from django import forms


class Menu(models.Model):
    typeMenu = models.ForeignKey(TypeMenu, blank=False, null=False)
    boisson = models.ForeignKey(Produit, blank=False, null=False, related_name="menu_boisson")
    plat = models.ForeignKey(Produit, blank=False, null=False, related_name="menu_plat")
    produit1 = models.ForeignKey(Produit, blank=False, null=False, related_name="menu_produit1")
    produit2 = models.ForeignKey(Produit, blank=True, null=True, related_name="menu_produit2")
    date = models.DateTimeField(auto_now_add = True, auto_now = True)
    panier = models.ForeignKey(Panier, blank=False, null=False)
    
    class Meta:
        app_label = 'Commun'

    def __unicode__(self):
       return "Menu {0} de {1}".format(self.typeMenu.nom, self.user.username);

class ChoisirMenuForm(forms.ModelForm):
    def __init__(self, plat, *args, **kwargs):
        super(ChoisirMenuForm, self).__init__(*args, **kwargs)
   
        cat_boisson = Categorie.objects.filter(nom="Boisson")
        cat_plat = Categorie.objects.filter(nom=plat)
        cat_article = Categorie.objects.all().exclude(nom__in=["Pizza", "Boisson", "Sandwich", "Quiche"])
        
        self.fields['boisson'] = forms.ModelChoiceField(Produit.objects.filter(categorie=cat_boisson).filter(quantite__gte=1))
        self.fields['plat'] = forms.ModelChoiceField(Produit.objects.filter(categorie=cat_plat).filter(quantite__gte=1))
        self.fields['produit1'] = forms.ModelChoiceField(Produit.objects.filter(categorie__in=cat_article).filter(quantite__gte=1))
        self.fields['produit2'] = forms.ModelChoiceField(Produit.objects.filter(categorie__in=cat_article).filter(quantite__gte=1))

    class Meta:
        model = Menu
        exclude=('typeMenu', 'date', 'panier')
