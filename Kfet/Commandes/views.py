# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Produit_Panier, Panier, Status_Commande, Commande, TypeMenu, Menu, ChoisirMenuForm, Commentaire, Categorie, ReglementCommandeForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


def produit(request, produit_id, erreur=None):
    user = request.user
    profile = user.get_profile()

    produit = get_object_or_404(Produit, pk=produit_id)
    produit.decimal=str(produit.prix%1).split(".")[1]

    if not user.is_anonymous():
        if request.method == 'POST':
            Com = Commentaire(profile_id=profile.id,commentaire=request.POST['com'],produit_id=produit_id)
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
    categorie = get_object_or_404(Categorie, pk=cat_id)
    context={}
    context['categorie']=categorie

    try:
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
        context['produit']=produits
    except Http404:
        pass

    return render_to_response('Commandes/categorie.html', context, context_instance=RequestContext(request) )

@login_required
def panier(request, erreur=None):
    user = request.user
    profil = user.get_profile()
    panier = Produit_Panier.objects.filter(panier=profil.panier_id)
    menus = profil.panier.menu_set.all()
    context = {}
    context['panier']=panier
    context['menus']=menus

    if erreur==None:
        pass
    elif erreur=="1":
        erreur = "<strong>Un produit ne peut pas être commandé avec une quantité nulle!</strong>. Veuillez le supprimer ou changer la quantité commandée"
    elif erreur=="2":
        erreur = "<strong>Un produit n'est plus en stock !</strong>. Veuillez le supprimer ou attendre un approvisionnement"
    elif erreur=="3":
        erreur = "<strong>Le panier est vide</strong>, veuillez ajoutez des articles dans le panier pour le valider"
    elif erreur=="4":
        erreur = "<strong>Un produit n'est pas en quantité suffisante !</strong>. Veuillez le supprimer, attendre un approvisionnement ou changer la quantité commandée"
    elif erreur=="10":
        erreur = "<strong>Le type de paiement est incorrect.</strong>"
    elif erreur=="11":
        erreur = "<strong>La quantité ne peut être supérieure au stock</strong>, veuillez choisir une valeur inférieure ou égale à la quantité restante."
    elif erreur=="12":
        erreur = "<strong>La quantité ne peut être nulle</strong>, veuillez sélectionner une valeur positive."
    else:
        erreur = "Une erreur est survenue, merci de réessayer"
    context['erreur']=erreur

    form = ReglementCommandeForm()
    context['form']=form

    return render_to_response('Commandes/panier.html', context, context_instance=RequestContext(request) )

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
def panier_menu_suppr(request, menu_id):
    Menu.objects.filter(id=menu_id).delete()
    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

@login_required
def panier_maj(request, produit_panier_id):
    if request.method == 'POST':
        produit_panier = get_object_or_404(Produit_Panier, pk=produit_panier_id)
        produit = get_object_or_404(Produit, pk=produit_panier.produit_id)
        quantite = request.POST['quantite']
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
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

    user = request.user # On récupère l'utilisateur
    profil = user.get_profile() # on récupère son profil
    panier_a_valider = profil.panier # on récupère son panier
    produits_a_valider = Produit_Panier.objects.filter(panier=profil.panier_id) # Le panier liste les produits sélectionnés
    menus = panier_a_valider.menu_set.all()
    prix_panier=0


    if produits_a_valider.count()<=0 and menus.count()<=0 :
        # Le panier est vide
        erreur=3
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))

    # On créé la commande
    commande = Commande()
    commande.prix = prix_panier
    commande.user = user
    commande.panier = panier_a_valider
    # On récupère le type de paiement
    form = ReglementCommandeForm(data=request.POST)
    if form.is_valid():
        commande.reglement = form.cleaned_data['reglement']
    else:
        # Type de paiement incorrect
        return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[10]))
    
    # On récupère le status de la commande : "En cours" pour la première étape
    try:
        status_encours = get_object_or_404(Status_Commande,label="En cours")
    except Http404:
        return HttpResponse("Aucun status de commande n'est défini (En Cours est celui par défaut)")
    commande.status_commande = status_encours

    if produits_a_valider.count()>0: # il y a des produits dans le panier
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

    if menus.count()>0:
        for menu in menus:
            produits = [menu.plat, menu.boisson, menu.produit1]
            if menu.typeMenu.nombreArticles==2:
                produits.append(menu.produit2)
            # Première passe pour vérifier le stock de tous les produits
            for p in produits:
                if p.quantite<=0:
                    # produit en rupture de stock
                    erreur=2
                    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier', args=[erreur]))
            # Deuxième pass pour diminuer le stock de tous les produits en même temps!
            for p in produits:
                # stock suffisant pour commander
                p.quantite -= 1  # on met à jour le stock
                p.save()
            prix_panier += menu.typeMenu.prix # On ajoute le prix


    commande.prix = prix_panier
    # On sauvegarde la commande une fois les stocks mis à jour
    commande.save()
    # On smet à jour la dette de l'utilisateur si il l'a choisit comme moyen de paiement
    if commande.reglement.type=="Dette":
        profil.dette += commande.prix
    profil.save()


    # On créé un nouveau panier pour l'utilisateur et le rattache à son profil
    nouveau_panier = Panier()
    nouveau_panier.save()
    profil.panier = nouveau_panier
    profil.save()

    return HttpResponseRedirect(reverse('Kfet.Commandes.views.confirmationPanier', args=[commande.id]))

@login_required
def choisirMenu(request, typeMenu_id, menu_id=None):
    typeMenu = get_object_or_404(TypeMenu, pk=typeMenu_id)
    if menu_id!=None:
        menu = get_object_or_404(Menu, pk=menu_id)
    else:
        menu = Menu()
        menu.typeMenu_id = typeMenu_id
        menu.panier = request.user.get_profile().panier
    
    if request.method=='POST':
        form = ChoisirMenuForm(plat=typeMenu.categorie.nom,data=request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))
    else:
        form = ChoisirMenuForm(plat=typeMenu.categorie.nom, instance=menu)
    return render_to_response('Commandes/choisirMenu.html', {'form':form, 'typeMenu':typeMenu, 'menu_id':menu.id}, context_instance=RequestContext(request))

@login_required
def confirmationPanier(request, commande_id):
    try:
        commande = Commande.objects.get(pk=commande_id)
    except Commande.DoesNotExist:
        return HttpResponse("Erreur pendant la validation du panier. La commande {0} n'existe pas.".format(commande_id))
    user = request.user
    if user!=commande.user:
        return HttpResponse("Cette commande ne vous appartient pas")

    panier_produit = Produit_Panier.objects.filter(panier=commande.panier)
    nbProduits = 0
    prixProduits = 0
    for pan in panier_produit:
        nbProduits+=pan.quantite
        prixProduits+=pan.quantite*pan.produit.prix

    menus = Menu.objects.filter(panier=commande.panier)
    prixMenus = 0
    for m in menus:
        prixMenus+=m.typeMenu.prix
    
    return render_to_response('Commandes/confirmationPanier.html', {'commande':commande, "panier_produit":panier_produit, "nbProduits":nbProduits, "menus":menus, "prixProduits":prixProduits, "prixMenus":prixMenus}, context_instance=RequestContext(request))


@login_required
def comm_suppr(request, comm_id):
    user = request.user
    profile = user.get_profile()

    comm = Commentaire.objects.get(pk=comm_id)
    produit = Produit.objects.get(pk=comm.produit_id)

    if profile.id == comm.profile_id or user.is_staff:
        comm.delete()        
    return HttpResponseRedirect(reverse('Kfet.Commandes.views.produit', args=[produit.id]))

@login_required
def comm_maj(request, comm_id):
    return HttpResponseRedirect(reverse('Kfet.Commandes.views.panier'))

