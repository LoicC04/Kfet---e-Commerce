from django.shortcuts import render_to_response, get_object_or_404
from Kfet.Commun.models import Produit, Categorie
from django.template import RequestContext

def produit(request, produit_id):
#    p = get_object_or_404(Poll, pk=poll_id)
    produit = Produit.objects.get(pk=produit_id)
    return render_to_response('Ventes/produit.html', {'produit':produit}, context_instance=RequestContext(request))

def categorie(request, cat_id):
#    p = get_object_or_404(Poll, pk=poll_id)
    categorie = Categorie.objects.get(pk=cat_id)
    produit = Produit.objects.filter(categorie=cat_id)
    return render_to_response('Ventes/categorie.html', {'produit':produit , 'categorie':categorie}, context_instance=RequestContext(request) )


#def index(request):
#    return HttpResponse("Hello, world. You're at the Ventes index.")
