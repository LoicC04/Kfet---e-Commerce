from django.db import models

class Reglement(models.Model):
        type = models.CharField(max_length=200)

