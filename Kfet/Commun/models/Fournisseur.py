# -*- coding: utf-8 -*- 
from django.db import models
from django import forms
from django.contrib.localflavor.fr.forms import FRPhoneNumberField


class Fournisseur(models.Model):
        nom = models.CharField(max_length=200)
        adresse = models.CharField(max_length=200)
        tel = models.CharField(max_length=14)
        mail = models.CharField(max_length=200)
        description = models.TextField()

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return self.nom;

class CreationForm(forms.ModelForm):
    class Meta:
        model = Fournisseur

    tel = FRPhoneNumberField(label='Téléphone',error_messages={'invalid': (u'Format du numéro de téléphone : 0X XX XX XX XX.')})
    mail = forms.EmailField()

