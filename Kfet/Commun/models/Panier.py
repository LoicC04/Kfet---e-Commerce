from django.db import models


class Panier(models.Model):
        date = models.DateTimeField(auto_now_add = True, auto_now = True)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return unicode(self.id);
