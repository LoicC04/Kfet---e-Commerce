from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Categorie, Produit_Panier
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render_to_response('Commandes/produit.html', {'produit':produit}, context_instance=RequestContext(request))

def categorie(request, cat_id):
    categorie = get_object_or_404(Produit, pk=cat_id)
    produit = get_list_or_404(Produit, categorie=cat_id)
    return render_to_response('Commandes/categorie.html', {'produit':produit , 'categorie':categorie}, context_instance=RequestContext(request) )

@login_required
def panier(request):
    user = request.user
    profil = user.get_profile()
    panier = Produit_Panier.objects.filter(panier_id=profil.panier_id)
    return render_to_response('Commandes/panier.html', {'panier':panier}, context_instance=RequestContext(request) )

@login_required
def panier_ajout(request):
    if request.method == 'POST':
        quantite = request.POST['quantite']
        produit_id = request.POST['produit']
        user = request.user
        profil = user.get_profile()
        produit_panier = Produit_Panier(quantite=quantite, produit_id=produit_id, panier=profil.panier)
        produit_panier.save()
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))
    else:
        return HttpResponseRedirect(reverse('Kfet.Commande.views.panier'))
