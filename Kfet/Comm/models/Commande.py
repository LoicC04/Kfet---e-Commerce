from django.db import models

from Personne import *
from Reglement import *
from Status_Commande import *

class Commande(models.Model):
        personne = models.ForeignKey(Personne)
        type = models.ForeignKey(Status_Commande)
        reglement = models.ForeignKey(Reglement)

	class Meta:
            app_label = 'Comm'
