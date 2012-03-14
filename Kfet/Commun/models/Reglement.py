from django.db import models


class Reglement(models.Model):
        type = models.CharField(max_length=200)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
           return self.type;
