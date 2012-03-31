# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from Kfet.Commun.models import Promo, Panier, Status_Commande, Commande
from Kfet.Commun.models.UserProfile import create_user_profile
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
                    panier = Panier()
                    panier.save()
                    user = User()
                    user.username = numero           
                    user.first_name = prenom
                    user.last_name = nom                   
                    user.email = mail
                    user.set_password(password)

                    try:
                        user.save()
                    except IntegrityError:
                        form.erreurNum = "Votre nom d'utilisateur existe déjà, veuillez vous connecter."                  

                    try:
                        create_user_profile(sender=User, instance=user,created=True,promo=promo,panier=panier)
                    except IntegrityError:
                        form.erreurNum = "Votre nom d'utilisateur existe déjà, veuillez vous connecter."                    
                    else:
                        return HttpResponseRedirect(reverse('Kfet.Comptes.views.login'))
                else: 
                    form.erreurMail = "Votre adresse email existe déjà veuillez vous connecter."

            else:
                form.erreurPass = "Les champs mot de passe ne correspondent pas."

    return render_to_response('Comptes/creation.html', {'form': form,}, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('Kfet.Comptes.views.gestion'))
            else:
                return HttpResponse('User inactif')                
                # Return a 'disabled account' error message
        else:
            erreur = "Utilisateur et/ou mot de passe incorrect"
            return render_to_response('Comptes/login.html', {'erreur':erreur}, context_instance=RequestContext(request)) 
            # Return an 'invalid login' error message.
    
    return render_to_response('Comptes/login.html', context_instance=RequestContext(request))

@login_required
def gestion(request):
    context={}
    user=request.user
    profile = user.get_profile()
    context['user'] = user
    context['profile'] = profile

    try:
        encours = Status_Commande.objects.get(code=1)
    except Status_Commande.DoesNotExist:
        encours=None
        #return HttpResponse("Aucun status de commande n'est défini n'est défini (En cours est celui par défaut)")
    if encours!=None:
        commandes = Commande.objects.filter(status_commande=encours)
    
        paginator = Paginator(commandes, 10) # Show 10 items per page
        page = request.GET.get('page',1)
        try:
            commandes_encours = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            commandes_encours = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            commandes_encours = paginator.page(paginator.num_pages)

        if commandes_encours.object_list.count()>0:
            context['commandes_encours'] = commandes_encours
    return render_to_response('Comptes/gestion.html', context,  context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('Kfet.views.home'))

