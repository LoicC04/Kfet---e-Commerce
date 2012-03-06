from django.db import models

class Information(models.Model):
        info = models.CharField(max_length=200)
