from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404, HttpResponse
from Kfet.Commun.models import Produit, CreationProduitForm
from Kfet.Commun.models import Fournisseur, CreationForm
from Kfet.Commun.models import Categorie, CreationCategorieForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import os
from django.utils.html import escape
from django.db.models.loading import get_models, get_apps
from django.forms.models import modelform_factory

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
        return  HttpResponseRedirect(reverse('Kfet.Comptes.views.login'))

@login_required
def reappro(request):
    list_Fournisseur = Fournisseur.objects.all()
    return render_to_response('GestionStock/reappro.html', { 'fournisseurs':list_Fournisseur, }, context_instance=RequestContext(request))

@login_required
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

@login_required
def commander(request, fournisseur_id, erreur=None):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    list_produits = Produit.objects.all().filter(fournisseur=fournisseur_id).order_by('quantite').filter(quantiteCommandeFournisseur__lte=0)
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
    return render_to_response('GestionStock/commander.html', {'form':form, 'fournisseur':fournisseur,'produits':produits, 'produits_commande':list_produits_commande, 'erreur':erreur }, context_instance=RequestContext(request))

@login_required
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

@login_required
def supprimerProduit(request, fournisseur_id, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    produit.delete()
    os.remove(produit.image.path)
    return  HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[fournisseur_id]))

@login_required
def editerCategorie(request, categorie_id=None):
    if categorie_id!=None:
        categorie = get_object_or_404(Categorie, pk=categorie_id)
    else:
        categorie = Categorie()
    
    if request.method=='POST':
        form = CreationCategorieForm(data=request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('Kfet.GestionStock.views.reappro'))
    else:
        form = CreationCategorieForm(instance=categorie)
    return render_to_response('GestionStock/creerCategorie.html', {'form':form , 'categorie_id':categorie_id}, context_instance=RequestContext(request))

@login_required
def add_new_model(request, model_name):
    if (model_name.lower() == model_name):
        normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name

    app_list = get_apps()
    for app in app_list:
        for model in get_models(app):
            if model.__name__ == normal_model_name:
                form = modelform_factory(model)

                if request.method == 'POST':
                    form = form(request.POST)
                    if form.is_valid():
                        try:
                            new_obj = form.save()
                        except forms.ValidationError, error:
                            new_obj = None

                        if new_obj:
                            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                (escape(new_obj._get_pk_val()), escape(new_obj)))

                else:
                    form = form()

                page_context = {'form': form, 'field': normal_model_name}
                return render_to_response('widgets/popup.html', page_context, context_instance=RequestContext(request))

@login_required
def commande(request, produit_id):
    if request.method == 'POST':
        produit = get_object_or_404(Produit, pk=produit_id)
        quantite = request.POST['quantiteCommandeFournisseur']
        if quantite:
            if int(quantite) <= 0:
                erreur = 1
                return HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[produit.fournisseur_id,erreur]),)
            else:
                Produit.objects.filter(id=produit_id).update(quantiteCommandeFournisseur=quantite)
                return HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[produit.fournisseur_id]),)
        else:
            erreur = 2
            return HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[produit.fournisseur_id,erreur]),)
    else:
        return HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[produit.fournisseur_id]),)

@login_required
def validerCommande(request, fournisseur_id):
    list_produits_commande = Produit.objects.all().filter(fournisseur=fournisseur_id).filter(quantiteCommandeFournisseur__gte=1)
    for p in list_produits_commande:
        p.quantite = p.quantite+p.quantiteCommandeFournisseur
        p.quantiteCommandeFournisseur = 0
        p.save()
    return HttpResponseRedirect(reverse('Kfet.GestionStock.views.commander', args=[fournisseur_id]),)
