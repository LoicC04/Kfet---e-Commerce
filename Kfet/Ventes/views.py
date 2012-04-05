# Create your views here.
from django.shortcuts import render_to_response, get_list_or_404
from Commun.models.Produit import *
from Commun.models.Vente import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request):
    list_produit = get_list_or_404(Produit)
    
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

    return render_to_response('Ventes/index.html', {'produit':produits}, context_instance=RequestContext(request) )

def produit_vente(request, produit_id):
    if request.method == 'POST':
        quantite = int(request.POST['quantite'])
    else:
        quantite = 1

    produit = Produit.objects.get(pk=produit_id)
    produit.quantite = produit.quantite - quantite
    produit.save()

    vente = Vente(produit_id=produit_id, quantite=quantite)
    vente.save()
    return HttpResponseRedirect(reverse('Kfet.Ventes.views.index'))


    

