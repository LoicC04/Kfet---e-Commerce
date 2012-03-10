from django.shortcuts import render_to_response
from Kfet.Commun.models import Produit


def index(request):
    list_produit = Produit.objects.all()
    return render_to_response('GestionStock/home.html', {'produits':list_produit})
