from django.db import models
from django import forms


class Reglement(models.Model):
        type = models.CharField(max_length=200, blank=False, null=False)
        proposeEnLigne = models.BooleanField(default=False, blank=False, null=False)
        actif = models.BooleanField(default=True, blank=False, null=False)

	class Meta:
            app_label = 'Commun'

        def __unicode__(self):
           return self.type;

class ReglementForm(forms.ModelForm):
    class Meta:
        model = Reglement
        exclude=('actif')
