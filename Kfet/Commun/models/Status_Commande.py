from django.db import models

class Status_Commande(models.Model):
        code = models.IntegerField()
        label = models.CharField(max_length=200)

	class Meta:
            app_label = 'Commun'
