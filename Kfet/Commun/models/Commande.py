from django.db import models
from Reglement import *
from Panier import *
from Status_Commande import *
from django.contrib.auth.models import User


class Commande(models.Model):
        user = models.ForeignKey(User)
        status_commande = models.ForeignKey(Status_Commande)
        reglement = models.ForeignKey(Reglement)
        panier = models.ForeignKey(Panier)
        prix = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
            return unicode(self.id);
