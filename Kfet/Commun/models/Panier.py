from django.db import models
from Menu import Menu


class Panier(models.Model):
        date = models.DateTimeField(auto_now_add = True, auto_now = True)
        menus = models.ManyToManyField(Menu)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
                   return unicode(self.id);
