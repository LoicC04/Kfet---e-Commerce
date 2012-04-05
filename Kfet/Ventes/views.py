# Create your views here.
from django.shortcuts import render_to_response, get_list_or_404
from Commun.models.Produit import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext


def index(request):
    list_produit = get_list_or_404(Produit)
    
    paginator = Paginator(list_produit, 10) # Show 10 items per page
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

