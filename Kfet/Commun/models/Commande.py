from django.db import models
from Reglement import Reglement
from Panier import Panier
from Status_Commande import Status_Commande
from django.contrib.auth.models import User
from django import forms


class Commande(models.Model):
        user = models.ForeignKey(User)
        status_commande = models.ForeignKey(Status_Commande)
        reglement = models.ForeignKey(Reglement)
        panier = models.ForeignKey(Panier)
        prix = models.DecimalField(max_digits=10, decimal_places=2)
        date = models.DateField(auto_now_add = True, auto_now = True)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
            return unicode(self.id);

class ReglementCommandeForm(forms.ModelForm):
    class Meta:
        model=Commande
        exclude=('user','status_commande','panier', 'prix', 'date')

    reglement = forms.ModelChoiceField(Reglement.objects.filter(proposeEnLigne=True))
