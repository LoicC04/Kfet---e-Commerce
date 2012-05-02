# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_list_or_404
from Commun.models.Produit import *
from Commun.models.Vente import *
from Commun.models.Promo import *
from Commun.models.UserProfile import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff)
def index(request, promo_id, open, erreur=None):
    list_produit = get_list_or_404(Produit)

    if erreur == "1":
        error = "Merci de spécifier un chiffre ou de cliquer directement sur le produit pour une vente unique."
    else:
        error = ""
    
    paginator = Paginator(list_produit, 12) # Show 10 items per page
    page = request.GET.get('page',1)
    try:
        produits = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        produits = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        produits = paginator.page(paginator.num_pages)
    
    try:
        vente = Vente.objects.latest('date')
    except Vente.DoesNotExist:         
        vente = Vente()

    promos = Promo.objects.all()
    users = UserProfile.objects.filter(promo=promo_id)

    if open == "1":
        open = 1

    return render_to_response('Ventes/index.html', {'produit':produits, 'vente':vente, 'error':error, 'promos':promos, 'users':users, 'open':open}, context_instance=RequestContext(request) )

@user_passes_test(lambda u: u.is_staff)
def produit_vente(request, produit_id):
    if request.method == 'POST':
        try:
            quantite = int(request.POST['quantite'])
        except ValueError:
            quantite = 0

        if quantite != 0:
            produit = Produit.objects.get(pk=produit_id)
            produit.quantite = produit.quantite - quantite
            produit.save()



            if request.POST['nomDette'] != "no":
                user = UserProfile.objects.get(user=request.POST['nomDette'])
                user.dette = user.dette + quantite * produit.prix
                user.save()

                vente = Vente(produit_id=produit_id, quantite=quantite, user_id=user.id)
                vente.save()

            else:
                vente = Vente(produit_id=produit_id, quantite=quantite)
                vente.save()

            return HttpResponseRedirect(reverse('Kfet.Ventes.views.index', args=["1","0"]))
    else:
        return HttpResponseRedirect(reverse('Kfet.Ventes.views.index', args=["1","0", "1"]))

@user_passes_test(lambda u: u.is_staff)   
def annuler_vente(request, vente_id):
    
    vente = Vente.objects.get(pk=vente_id)

    produit = Produit.objects.get(pk=vente.produit.id)
    produit.quantite = produit.quantite + vente.quantite
    produit.save()

    if vente.user_id:
        user = UserProfile.objects.get(pk=vente.user_id)
        user.dette = user.dette - vente.quantite * produit.prix
        user.save()


    vente.delete()

    return HttpResponseRedirect(reverse('Kfet.Ventes.views.index', args=["1","0"]))

