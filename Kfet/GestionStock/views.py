from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from Kfet.Commun.models import Produit, CreationProduitForm
from Kfet.Commun.models import Fournisseur, CreationForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import os

@login_required
def index(request):
    user = request.user
    if user.is_staff:
        list_produit_rupture = Produit.objects.all().filter(quantite=0)
        list_produit_en_stock = Produit.objects.all().filter(quantite__gte=1)

        paginator_rupture = Paginator(list_produit_rupture, 10) # Show 10 items per page
        paginator_stock = Paginator(list_produit_en_stock, 10) # Show 10 items per page

        page_rupture = request.GET.get('pageRupture',1)
        page_stock = request.GET.get('pageStock',1)
        try:
            produits_rupture = paginator_rupture.page(page_rupture)
            produits_stock = paginator_stock.page(page_stock)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            produits_rupture = paginator_rupture.page(1)
            produits_stock = paginator_stock.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            produits_rupture = paginator_rupture.page(paginator_rupture.num_pages)
            produits_stock = paginator_stock.page(paginator_stock.num_pages)

        return render_to_response('GestionStock/home.html', {'produits_out':produits_rupture, 'produits_in':produits_stock}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

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

def commander(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    list_produits = Produit.objects.all().filter(fournisseur=fournisseur_id).order_by('quantite')
    list_produits_commande = Produit.objects.all().filter(fournisseur=fournisseur_id).filter(quantiteCommandeFournisseur__gte=1).order_by('quantite')

    paginator = Paginator(list_produits, 10) # Show 10 items per page
    page = request.GET.get('page',1)
    try:
        produits = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        produits = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        produits = paginator.page(paginator.num_pages)

    form=None
    return render_to_response('GestionStock/commander.html', {'form':form, 'fournisseur':fournisseur,'produits':produits, 'produits_commande':list_produits_commande}, context_instance=RequestContext(request))

def creerProduit(request, fournisseur_id, produit_id=None):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    if produit_id!=None:
        produit = get_object_or_404(Produit, pk=produit_id)
    else:
        produit = Produit()
        produit.fournisseur_id = fournisseur_id
    
    if request.method=='POST':
        form = CreationProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[fournisseur_id]))
    else:
        form = CreationProduitForm(instance=produit)

    return render_to_response('GestionStock/creerProduit.html', {'form':form, 'fournisseur':fournisseur, 'produit_id':produit.id}, context_instance=RequestContext(request))

def supprimerProduit(request, fournisseur_id, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    produit.delete()
    os.remove(produit.image.path)
    return  HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[fournisseur_id]))

