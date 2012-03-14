from django.db import models


class Panier(models.Model):
        date = models.DateTimeField('date vente')

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return unicode(self.id);
