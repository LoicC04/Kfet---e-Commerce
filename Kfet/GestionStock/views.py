from django.shortcuts import render_to_response
from Kfet.Commun.models import Produit
from Kfet.Commun.models import Fournisseur
from django.template import RequestContext


def index(request):
    list_produit_rupture = Produit.objects.all().filter(quantite=0)
    list_produit_en_stock = Produit.objects.all().filter(quantite__gte=1)
    return render_to_response('GestionStock/home.html', {'produits_out':list_produit_rupture, 'produits_in':list_produit_en_stock}, context_instance=RequestContext(request))

def reappro(request):
    list_Fournisseur = Fournisseur.objects.all()
    return render_to_response('GestionStock/reappro.html', { 'fournisseurs':list_Fournisseur, }, context_instance=RequestContext(request))

def creerFournisseur(request):
    return render_to_response('GestionStock/creerFournisseur.html', { }, context_instance=RequestContext(request))
