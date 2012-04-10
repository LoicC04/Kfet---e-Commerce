# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from Kfet.Commun.models.TypeMenu import TypeMenu, TypeMenuForm
from Kfet.Commun.models.Commande import Commande
from Kfet.Commun.models.Reglement import Reglement, ReglementForm
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse


@login_required
def index(request):
    return render_to_response('Administration/index.html', { }, context_instance=RequestContext(request))

@login_required
def typeMenu(request, erreur=None):
    menus_actif = TypeMenu.objects.filter(actif=True)
    menus_inactif = TypeMenu.objects.filter(actif=False)
    context={}
    context['menus_actif']=menus_actif
    context['menus_inactif']=menus_inactif
    if erreur=="1":
        context['erreur']="Des ventes ont été effectuées avec ce menu, impossible de le supprimer. Il peut être désactiver"
    return render_to_response('Administration/typeMenu.html', context, context_instance=RequestContext(request))

@login_required
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

@login_required
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

def activerMenu(request, menu_id):
    typeMenu = get_object_or_404(TypeMenu, pk=menu_id)
    typeMenu.actif=True
    typeMenu.save()
    return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeMenu'))

@login_required
def typeReglement(request, erreur=None):
    context = {}
    reglements = Reglement.objects.all().filter(actif=True)
    context['reglements']=reglements
    if erreur=="1":
        context['erreur']="Le type de régèlement est désactivé"
    return render_to_response('Administration/typeReglement.html', context, context_instance=RequestContext(request))

@login_required
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

@login_required
def supprimerReglement(request, reglement_id):
    reglement = Reglement.objects.get(pk=reglement_id)
    reglement.actif=False
    reglement.save()
    erreur="Le règlement a été désactivé"
    return render_to_response('Administration/typeReglement.html', {'erreur':erreur}, context_instance=RequestContext(request))

@login_required
def dettes(request):
    return render_to_response('Administration/dettes.html', { }, context_instance=RequestContext(request))
