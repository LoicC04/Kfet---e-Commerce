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
        password = forms.CharField(label=('Mot de passe'),widget=forms.PasswordInput(render_value=False), required=True) 
        mail = forms.EmailField(label="Adresse email", required=True)
        promo = forms.ModelChoiceField(queryset=Promo.objects.all())

def creation(request):
    if request.method == 'POST': 
        form = CompteForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            password = form.cleaned_data['password']
            mail = form.cleaned_data['mail']
            promo = form.cleaned_data['promo']
            
            personne = Personne(num_etu=numero, nom=nom, prenom=prenom, password=password, mail=mail, promo=promo)
            personne.save()

            return HttpResponseRedirect('/comptes/ok/')
    else:
        form = CompteForm()

    return render_to_response('Comptes/creation.html', {'form': form,}, context_instance=RequestContext(request))

def ok(request):
    return HttpResponse('Hey')
