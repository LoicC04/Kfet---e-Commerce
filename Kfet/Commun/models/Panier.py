from django.db import models

from Date import *

class Panier(models.Model):
        date = models.ForeignKey(Date)

	class Meta:
            app_label = 'Comm'
