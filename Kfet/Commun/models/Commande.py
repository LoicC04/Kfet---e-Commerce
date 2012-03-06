from django.db import models

class Commande(models.Model):
        personne = models.ForeignKey(Personne)
        type = models.ForeignKey(Status_Commande)
        reglement = models.ForeignKey(Reglement)

