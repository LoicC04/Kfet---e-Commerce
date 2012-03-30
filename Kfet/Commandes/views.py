# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Produit_Panier, Panier, Status_Commande, Commande, Reglement, TypeMenu, Menu, ChoisirMenuForm, Commentaire
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


def produit(request, produit_id, erreur=None):
    user = request.user
    produit = get_object_or_404(Produit, pk=produit_id)
    produit.decimal=str(produit.prix%1).split(".")[1]

    if not user.is_anonymous():
        if request.method == 'POST':
            Com = Commentaire(user_id=user.id,commentaire=request.POST['com'],produit_id=produit_id)
            Com.save()

    list_comms = Commentaire.objects.filter(produit=produit_id)

    paginator = Paginator(list_comms, 4)
    page = request.GET.get('page',1)
    try:
        comms = paginator.page(page)
    except PageNotAnInteger:
        comms = paginator.page(1)
    except EmptyPage:
        comms = paginator.page(paginator.num_pages)

    return render_to_response('Commandes/produit.html', {'produit':produit, 'erreur':erreur, 'comms':comms}, context_instance=RequestContext(request))

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
    elif erreur=="1":
        erreur = "<strong>Un produit ne peut pas être commandé avec une quantité nulle!</strong>. Veuillez le supprimer ou changer la quantité commandée"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="2":
        erreur = "<strong>Un produit n'est plus en stock !</strong>. Veuillez le supprimer ou attendre un approvisionnement"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="3":
        erreur = "<strong>Le panier est vide</strong>, veuillez ajoutez des articles dans le panier pour le valider"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="4":
        erreur = "<strong>Un produit n'est pas en quantité suffisante !</strong>. Veuillez le supprimer, attendre un approvisionnement ou changer la quantité commandée"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="10":
        erreur = "10"
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="11":
        erreur = "<strong>La quantité ne peut être supérieure au stock</strong>, veuillez choisir une valeur inférieure ou égale à la quantité restante."
        return render_to_response('Commandes/panier.html', {'panier':panier, 'erreur':erreur}, context_instance=RequestContext(request) )
    elif erreur=="12":
        erreur = "<strong>La quantité ne peut être nulle</strong>, veuillez sélectionner une valeur positive."
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
            if produit.quantite >= int(quantite):
                if int(quantite) <= 0:
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
        produit_panier = get_object_or_404(Produit_Panier, pk=produit_panier_id)
        produit = get_object_or_404(Produit, pk=produit_panier.produit_id)
        quantite = quantite=request.POST['quantite']
        if quantite:       
            if produit.quantite >= int(quantite):
                if int(quantite) <= 0:
                    erreur = 12
                    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
                else:
                    produit = Produit_Panier.objects.filter(id=produit_panier_id).update(quantite=quantite)
                    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))
            else:
                erreur = 11
                return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
        else:
            erreur = 12
            return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
    else:
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

@login_required
def validerPanier(request):
    user = request.user # On récupère l'utilisateur
    profil = user.get_profile() # on récupère son profil
    panier_a_valider = profil.panier # on récupère son panier
    produits_a_valider = Produit_Panier.objects.filter(panier=profil.panier_id) # Le panier liste les produits sélectionnés
    prix_panier=0


    if produits_a_valider.count()<=0:
        # Le panier est vide
        erreur=3
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))

    # On créé la commande
    commande = Commande()
    commande.prix = prix_panier
    commande.user = user
    commande.panier = panier_a_valider
    try:
        reglement_liquide = Reglement.objects.get(type="Liquide")
    except Reglement.DoesNotExist:
        return HttpResponse("Aucun type de règlement n'est défini (Liquide est celui par défaut)")
    commande.reglement = reglement_liquide
    try:
        status_encours = get_object_or_404(Status_Commande,label="En cours")
    except Http404:
        return HttpResponse("Aucun status de commande n'est défini (En Cours est celui par défaut)")
    commande.status_commande = status_encours

    for elt in produits_a_valider: # Pour chaque produit dans le panier on vérifie sa quantité par rapport au stock
        if elt.quantite<=0:
            # Un produit dans le panier a une quantité à 0
            erreur=1
            return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
        elif elt.produit.quantite<=0:
            # produit en rupture de stock
            erreur=2
            return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
        elif elt.quantite<=elt.produit.quantite:
            # stock suffisant pour commander
            prix_panier += elt.produit.prix*elt.quantite # On ajoute le prix*quantité
            elt.produit.quantite -= elt.quantite # on met à jour le stock
            elt.produit.save()
        else:
            # stock du produit insuffisant
            erreur=4
            return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))

    commande.prix = prix_panier
    # On sauvegarde la commande une fois les stocks mis à jour
    commande.save()

    # On créé un nouveau panier pour l'utilisateur et le rattache à son profil
    nouveau_panier = Panier()
    nouveau_panier.save()
    profil.panier = nouveau_panier
    profil.save()

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
