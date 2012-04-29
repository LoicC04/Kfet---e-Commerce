# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from Kfet.Commun.models.TypeMenu import TypeMenu, TypeMenuForm
from Kfet.Commun.models.Commande import Commande
from Kfet.Commun.models.Reglement import Reglement, ReglementForm
from Kfet.Commun.models.Vente import Vente
from Kfet.Commun.models.Promo import Promo
from Kfet.Commun.models.UserProfile import UserProfile
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
import datetime
import time
from django.utils.encoding import smart_str
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render_to_response('Administration/index.html', { }, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def typeMenu(request, erreur=None):
    menus_actif = TypeMenu.objects.filter(actif=True)
    menus_inactif = TypeMenu.objects.filter(actif=False)
    context={}
    context['menus_actif']=menus_actif
    context['menus_inactif']=menus_inactif
    if erreur=="1":
        context['erreur']="Des ventes ont été effectuées avec ce menu, impossible de le supprimer. Il peut être désactiver"
    return render_to_response('Administration/typeMenu.html', context, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def ajouterModifierMenu(request, menu_id=None):
    if menu_id!=None:
        menu = get_object_or_404(TypeMenu, pk=menu_id)
    else:
        menu = TypeMenu()
    
    if request.method=='POST':
        form = TypeMenuForm(data=request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeMenu'))
    else:
        form = TypeMenuForm(instance=menu)
    return render_to_response('Administration/ajouterModifierMenu.html', {'form':form , 'menu_id':menu_id}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def supprimerMenu(request,menu_id):
    """ Fonction de suppression des menus de la carte de la Kfet """
    # On récupère le typeMenu en question
    typeMenu = get_object_or_404(TypeMenu, pk=menu_id)
    if typeMenu.menu_set.count()==0:
        # Si aucun Menu n'a été créé avec ce typeMenu alors on le supprime
        typeMenu.delete()
        return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeMenu'))
    else:
        # Sinon, on vérifie pour chacun de ces menus, s'ils existent dans une commande. Si un meu n'existe pas dans une commande, c'est qu'il est dans le panier de quelqu'un
        # Alors, on supprime ce menu du panier de l'utilisateur et on déactive ce TypeMenu
        menus=typeMenu.menu_set.all()
        for m in menus:
            p = m.panier
            if Commande.objects.filter(panier=p).count()==0:
                m.delete()

        typeMenu.actif=False
        typeMenu.save()
        erreur=1
        
        return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeMenu', args=[erreur]))

@user_passes_test(lambda u: u.is_superuser)
def activerMenu(request, menu_id):
    typeMenu = get_object_or_404(TypeMenu, pk=menu_id)
    typeMenu.actif=True
    typeMenu.save()
    return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeMenu'))

@user_passes_test(lambda u: u.is_superuser)
def typeReglement(request, erreur=None):
    context = {}
    reglements = Reglement.objects.all().filter(actif=True)
    context['reglements']=reglements
    if erreur=="1":
        context['erreur']="Le type de régèlement est désactivé"
    return render_to_response('Administration/typeReglement.html', context, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def ajouterModifierReglement(request, reglement_id=None):
    if reglement_id!=None:
        reglement = get_object_or_404(Reglement, pk=reglement_id)
    else:
        reglement = Reglement()
    
    if request.method=='POST':
        form = ReglementForm(data=request.POST, instance=reglement)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeReglement'))
    else:
        form = ReglementForm(instance=reglement)
    return render_to_response('Administration/ajouterModifierReglement.html', {'form':form , 'reglement_id':reglement_id}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def supprimerReglement(request, reglement_id):
    reglement = Reglement.objects.get(pk=reglement_id)
    reglement.actif=False
    reglement.save()
    erreur="Le règlement a été désactivé"
    return render_to_response('Administration/typeReglement.html', {'erreur':erreur}, context_instance=RequestContext(request))



class DetteForm(forms.Form):
    dette_a_enlever = forms.DecimalField(max_digits=5, decimal_places=2,  widget=forms.TextInput(attrs={'size':'8'}))

@user_passes_test(lambda u: u.is_superuser)
def dettes(request, user_id=None, montant=None):
    context={}
    context["form"] = DetteForm()

    # Traitement du filtrage demandé par l'utilisateur
    promos = ["Tous"]
    promos.extend(Promo.objects.all())
    context['promos'] = promos
    promotion = request.GET.get('promo','Tous')
    users = UserProfile.objects.filter(dette__gt=0).order_by("-dette")
    if promotion!="Tous":
        try:
            promo = Promo.objects.get(promo=promotion)
            users = users.filter(promo=promo)
        except ObjectDoesNotExist:
            pass
    context['promo'] = promotion


    # Affichage des messages en fonctions des actions réalisées
    if user_id!=None:
        if user_id==-1:
            context["message"]="Erreur lors de la saisie de la dette"
        else:
            profile = UserProfile.objects.get(user=user_id)
            if montant!=None:
                context["message"]="La dette de {0} {1} a été diminuée de {2} €".format(smart_str(profile.user.first_name), smart_str(profile.user.last_name), montant)
            else:
                context["message"]="La dette de {0} {1} a été effacée".format(smart_str(profile.user.first_name), smart_str(profile.user.last_name))
    

    # Pagination des utilisateurs ayant des dettes
    paginator = Paginator(users,15) # Afficher 15 éléments par page
    page = request.GET.get('page',1)
    try:
        users_pagi = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, on affiche la première page
        users_pagi = paginator.page(1)
    except EmptyPage:
        # Si on dépasse le nombre de page, on affiche la dernière
        users_pagi = paginator.page(paginator.num_pages)

    context['users'] = users_pagi

    return render_to_response('Administration/dettes.html', context, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def effacerDette(request,user_id):
    profile = UserProfile.objects.get(user=user_id)
    profile.dette = 0
    profile.save()
    return dettes(request, user_id=profile.user.id)

@user_passes_test(lambda u: u.is_superuser)
def enleverDeDette(request, user_id):
    if request.method == "POST":
        profile = UserProfile.objects.get(user=user_id)
        form = DetteForm(data=request.POST)
        if form.is_valid():
            dette_a_enlever = form.cleaned_data['dette_a_enlever']
            profile.dette = profile.dette - dette_a_enlever
            profile.save()
            return dettes(request, user_id=profile.user.id, montant=dette_a_enlever)
    return dettes(request, user_id=-1)

@user_passes_test(lambda u: u.is_superuser)
def ventes(request):
    if request.method == "POST":

        date = time.strptime(request.POST['date'], "%m/%d/%Y")
        date = time.strftime("%Y-%m-%d", date)

        ventes = Vente.objects.filter(date=date)
        commandes = Commande.objects.filter(date=date)
        ca = 0
        for vente in ventes:
            ca += vente.produit.prix * vente.quantite

        for commande in commandes:
            ca += commande.prix

        return render_to_response('Administration/ventes.html', { 'ventes':ventes, 'commandes':commandes, 'ca':ca , 'date':date}, context_instance=RequestContext(request))

    else:
        ventes = Vente.objects.filter(date=datetime.date.today())
        commandes = Commande.objects.filter(date=datetime.date.today())
        ca = 0
        for vente in ventes:
            ca += vente.produit.prix * vente.quantite

        for commande in commandes:
            ca += commande.prix

        return render_to_response('Administration/ventes.html', { 'ventes':ventes, 'commandes':commandes, 'ca':ca }, context_instance=RequestContext(request))
