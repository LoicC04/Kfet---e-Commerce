from django.db import models

class Menu(models.Model):
        nom = models.CharField(max_length=200)

	class Meta:
            app_label = 'Comm'
