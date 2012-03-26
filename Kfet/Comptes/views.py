# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Promo, Personne, UserProfile
from Kfet.Commun.models.UserProfile import create_user_profile
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


class CompteForm(forms.Form):
        numero = forms.CharField(max_length=9, label="Numéro", required=True)
        nom = forms.CharField(max_length=200, label="Nom", required=True)
        prenom = forms.CharField(max_length=200, label="Prenom", required=True)
        password = forms.CharField(label=('Mot de passe'),widget=forms.PasswordInput(render_value=False), required=True) 
        password2 = forms.CharField(label=('Mot de passe'),widget=forms.PasswordInput(render_value=False), required=True) 
        mail = forms.EmailField(label="Adresse email", required=True)
        promo = forms.ModelChoiceField(queryset=Promo.objects.all())

def creation(request):    
    form = CompteForm()
    if request.method == 'POST': 
        form = CompteForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            mail = form.cleaned_data['mail']
            promo = form.cleaned_data['promo']

            if password == password2:                

                if User.objects.filter(email=mail).count() == 0:                        
                    user = User()
                    user.username = numero           
                    user.first_name = nom
                    user.last_name = prenom                   
                    user.email = mail
                    user.set_password(password)

                    try:
                        user.save()
                    except IntegrityError:
                        form.erreurNum = "Votre nom d'utilisateur existe déjà, veuillez vous connecter."                   

                    try:
                        create_user_profile(sender=User, instance=user,created=True,promo=promo)
                    except IntegrityError:
                        form.erreurNum = "Votre nom d'utilisateur existe déjà, veuillez vous connecter."                    
                    else:
                        return HttpResponse('Hey')
                else: 
                    form.erreurMail = "Votre adresse email existe déjà veuillez vous connecter."

            else:
                form.erreurPass = "Les champs mot de passe ne correspondent pas."

    return render_to_response('Comptes/creation.html', {'form': form,}, context_instance=RequestContext(request))

def ok(request):
    return HttpResponse('Hey')

def login(request):
    if request.method == 'POST':        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponse('Hey')
            else:
                return HttpResponse('User inactif')                
                # Return a 'disabled account' error message
        else:
            return render_to_response('Comptes/login.html', context_instance=RequestContext(request)) 
            # Return an 'invalid login' error message.
    
    return render_to_response('Comptes/login.html', context_instance=RequestContext(request))

@login_required
def gestion(request):
    user=request.user
    profile = user.get_profile()
    return render_to_response('Comptes/gestion.html', {'user':user,'profile':profile}, context_instance=RequestContext(request))

