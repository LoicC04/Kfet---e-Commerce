# -*- coding: utf-8 -*-
from django.db import models


class Status_Commande(models.Model):
        code = models.IntegerField()
        label = models.CharField(max_length=200)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
            return unicode(self.label);
