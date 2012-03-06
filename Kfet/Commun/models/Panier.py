from django.db import models

class Panier(models.Model):
        date = models.ForeignKey(Date)

