from django.db import models

class Date(models.Model):
        models.DateTimeField('date vente')

	class Meta:
            app_label = 'Comm'
