from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Categorie
from django.template import RequestContext
from django.http import HttpResponse


def produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render_to_response('Commandes/produit.html', {'produit':produit}, context_instance=RequestContext(request))

def categorie(request, cat_id):
    categorie = get_object_or_404(Produit, pk=cat_id)
    produit = get_list_or_404(Produit, categorie=cat_id)
    return render_to_response('Commandes/categorie.html', {'produit':produit , 'categorie':categorie}, context_instance=RequestContext(request) )


def panier(request):
    return HttpResponse("Hello, world. You're at the Ventes index.")
