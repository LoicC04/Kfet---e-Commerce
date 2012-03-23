# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Promo, Personne
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django import forms


class CompteForm(forms.Form):
        numero = forms.CharField(max_length=9, label="Numéro", required=True)
        nom = forms.CharField(max_length=200, label="Nom", required=True)
        prenom = forms.CharField(max_length=200, label="Prenom", required=True)
        password = forms.CharField(max_length=200, label="Mot de passe", required=True)
        mail = forms.EmailField(label="Adresse email", required=True)
        promo = forms.ChoiceField(label="Promotion", required=True)

def creation(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CompteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponse('Hey') # Redirect after POST
    else:
        form = CompteForm() # An unbound form

    return render_to_response('Comptes/creation.html', {'form': form,})

def ok(request):
    return HttpResponse('Hey')
