# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from Kfet.Commun.models.TypeMenu import TypeMenu, TypeMenuForm
from Kfet.Commun.models.Commande import Commande
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse


@login_required
def index(request):
    return render_to_response('Administration/index.html', { }, context_instance=RequestContext(request))

@login_required
def typeMenu(request, erreur=None):
    menus = TypeMenu.objects.filter(actif=True)
    context={}
    context['menus']=menus
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

@login_required
def typePaiement(request):
    return render_to_response('Administration/typePaiement.html', { }, context_instance=RequestContext(request))

@login_required
def dettes(request):
    return render_to_response('Administration/dettes.html', { }, context_instance=RequestContext(request))