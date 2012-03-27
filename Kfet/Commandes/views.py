from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Categorie, Produit_Panier
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User


def produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render_to_response('Commandes/produit.html', {'produit':produit}, context_instance=RequestContext(request))

def categorie(request, cat_id):
    categorie = get_object_or_404(Produit, pk=cat_id)
    produit = get_list_or_404(Produit, categorie=cat_id)
    return render_to_response('Commandes/categorie.html', {'produit':produit , 'categorie':categorie}, context_instance=RequestContext(request) )


def panier(request):
    user = request.user
    profil = user.get_profile()
    panier = Produit_Panier.objects.filter(panier_id=profil.panier_id)
    return render_to_response('Commandes/panier.html', {'panier':panier}, context_instance=RequestContext(request) )

def panier_ajout(request, quantite, produit_id):
    user = request.user
    profil = user.get_profile()
    produit_panier = Produit_Panier(quantite=quantite, produit_id=produit_id, panier_id=profil.panier_id)
    produit_panier.save()
    return HttpResponse('FUUU')
