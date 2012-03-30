# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Produit_Panier, Panier, Status_Commande, Commande, Reglement, TypeMenu, Menu, ChoisirMenuForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def produit(request, produit_id, erreur=None):
    produit = get_object_or_404(Produit, pk=produit_id)
    produit.decimal=str(produit.prix%1).split(".")[1]
    return render_to_response('Commandes/produit.html', {'produit':produit, 'erreur':erreur}, context_instance=RequestContext(request))

def categorie(request, cat_id):
    categorie = get_object_or_404(Produit, pk=cat_id)
    list_produit = get_list_or_404(Produit, categorie=cat_id)
    
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

    return render_to_response('Commandes/categorie.html', {'produit':produits , 'categorie':categorie}, context_instance=RequestContext(request) )

@login_required
def panier(request, erreur=None):
    user = request.user
    profil = user.get_profile()
    panier = Produit_Panier.objects.filter(panier=profil.panier_id)
    if erreur==None:
        return render_to_response('Commandes/panier.html', {'panier':panier}, context_instance=RequestContext(request) )
    elif erreur=="3":
        erreur = "<strong>Le panier est vide</strong>, veuillez ajoutez des articles dans le panier pour le valider"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="2":
        erreur = "<strong>Un produit n'est plus en stock !</strong>. Veuillez le supprimer ou attendre un approvisionnement"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="1":
        erreur = "<strong>Un produit n'est pas en quantité suffisante !</strong>. Veuillez le supprimer, attendre un approvisionnement ou changer la quantité commandée"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    else:
        erreur = "Une erreur est survenue, merci de réessayer"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )

@login_required
def panier_ajout(request):    
    if request.method == 'POST':        
        quantite = request.POST['quantite']
        produit_id = request.POST['produit']
        user = request.user
        profil = user.get_profile()
        produit = get_object_or_404(Produit, pk=produit_id)
        if quantite:
            if produit.quantite > int(quantite):
                if quantite == "0":
                    erreur = 1
                    return HttpResponseRedirect(reverse('Kfet.Commandes.views.produit', args=[produit_id,erreur]), )
                else:
                    produit_panier = Produit_Panier(quantite=quantite, produit_id=produit_id, panier=profil.panier)
                    produit_panier.save()
                return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))
            else:
                erreur = 2
                return HttpResponseRedirect(reverse('Kfet.Commandes.views.produit', args=[produit_id,erreur]), )
        else:
            erreur = 1
            return HttpResponseRedirect(reverse('Kfet.Commandes.views.produit', args=[produit_id,erreur]), )
    else:
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

@login_required
def panier_suppr(request, produit_panier_id):
    Produit_Panier.objects.filter(id=produit_panier_id).delete()
    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

@login_required
def panier_maj(request, produit_panier_id):
    if request.method == 'POST':
        produit = Produit_Panier.objects.filter(id=produit_panier_id).update(quantite=request.POST['quantite'])
    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

@login_required
def validerPanier(request):
    user = request.user
    profil = user.get_profile()
    panier_a_valider = profil.panier
    produits_a_valider = Produit_Panier.objects.filter(panier=profil.panier_id)
    prix_panier=0
    if produits_a_valider.count()>0:
        for elt in produits_a_valider:
            if elt.produit.quantite>=elt.quantite:
                # stock suffisant pour commander
                prix_panier += elt.produit.prix*elt.quantite
                elt.produit.quantite -= elt.quantite
                elt.produit.save()
            elif elt.quantite<=0:
                # Un produit dans le panier a une quantité à 0
                erreur=1
                return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
            elif elt.produit.quantite<=0:
                # stock pas suffisant pour un produit
                erreur=2
                return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))

        commande = Commande()
        commande.prix = prix_panier
        commande.user = user
        commande.panier = panier_a_valider
        commande.reglement = Reglement.objects.get(type="Liquide")
        commande.status_commande = Status_Commande.objects.get(label="En cours")

        commande.save()

        nouveau_panier = Panier()
        nouveau_panier.save()

        profil.panier = nouveau_panier
        profil.save()
    else:
        # Le panier est vide
        erreur=3
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))

    return HttpResponse("Valider! Prix à payer: {0} €".format(prix_panier))

@login_required
def choisirMenu(request,typeMenu_id, menu_id=None):
    typeMenu = get_object_or_404(TypeMenu, pk=typeMenu_id)
    if menu_id!=None:
        menu = get_object_or_404(Menu, pk=menu_id)
        menu_id=int(menu.id)
    else:
        menu = Menu()
        menu.typeMenu_id = typeMenu_id
        menu.user = request.user
    
    if request.method=='POST':
        form = ChoisirMenuForm(data=request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Kfet.views.home'))
    else:
        form = ChoisirMenuForm(instance=menu)
    return render_to_response('Commandes/choisirMenu.html', {'form':form, 'typeMenu':typeMenu}, context_instance=RequestContext(request))

