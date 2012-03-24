from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from Kfet.Commun.models import Produit
from Kfet.Commun.models import Fournisseur, CreationForm
from django.template import RequestContext
from django.core.urlresolvers import reverse


def index(request):
    list_produit_rupture = Produit.objects.all().filter(quantite=0)
    list_produit_en_stock = Produit.objects.all().filter(quantite__gte=1)
    return render_to_response('GestionStock/home.html', {'produits_out':list_produit_rupture, 'produits_in':list_produit_en_stock}, context_instance=RequestContext(request))

def reappro(request):
    list_Fournisseur = Fournisseur.objects.all()
    return render_to_response('GestionStock/reappro.html', { 'fournisseurs':list_Fournisseur, }, context_instance=RequestContext(request))

def creerFournisseur(request, id=None):
    if id!=None:
        fournisseur = get_object_or_404(Fournisseur, pk=id)
        id=int(fournisseur.id)
    else:
        fournisseur = Fournisseur()
    
    if request.method=='POST':
        form = CreationForm(data=request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('Kfet.GestionStock.views.reappro'))
    else:
        form = CreationForm(instance=fournisseur)

    return render_to_response('GestionStock/creerFournisseur.html', {'form':form , 'id':id}, context_instance=RequestContext(request))
