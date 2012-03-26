# -*- coding: utf-8 -*- 
from django.db import models
from django import forms
from Menu import *
from Categorie import *	
from Fournisseur import *
from PIL import Image


class Produit(models.Model):
        nom = models.CharField(max_length=200)
        prix = models.DecimalField(max_digits=10, decimal_places=2)
        menu = models.ForeignKey(Menu, blank=True, null=True)
        info = models.TextField()
        categorie = models.ForeignKey(Categorie)
        image = models.ImageField(upload_to="images/produits/", help_text="image 238x234px")
        quantite = models.IntegerField(default=0)
        quantiteCommandeFournisseur = models.IntegerField(default=0)
        fournisseur = models.ForeignKey(Fournisseur,blank=False, null=False)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
            representation = "{0}, quantite={1}".format(self.nom,self.quantite)
            return representation

        def save(self, size=(234,238)):
            super(Produit, self).save() 
            if self.image: 
                imagename = self.image.path
                image = Image.open(imagename)
                wpercent = (size[1]/float(image.size[1]))
                wsize = int((float(image.size[0])*float(wpercent)))
                image.thumbnail((wsize,size[1]))
                image.save(imagename)


class CreationProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude=('fournisseur', 'quantite', 'quantiteCommandeFournisseur')

