from django.db import models
from Reglement import Reglement
from Panier import Panier
from Status_Commande import Status_Commande
from Menu import Menu
from django.contrib.auth.models import User


class Commande(models.Model):
        user = models.ForeignKey(User)
        status_commande = models.ForeignKey(Status_Commande)
        reglement = models.ForeignKey(Reglement)
        panier = models.ForeignKey(Panier)
        prix = models.DecimalField(max_digits=10, decimal_places=2)
        date = models.DateTimeField(auto_now_add = True, auto_now = True)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
            return unicode(self.id);
