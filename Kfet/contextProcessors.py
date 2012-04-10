from Kfet.Commun.models import Categorie
from Kfet.Commun.models import Produit, Produit_Panier
from django.conf import settings


def categories(request):
    list = Categorie.objects.all()
    return { 'categories_list': list }

def articles(request):
    user = request.user
    prix=0
    decimal=0
    if not user.is_anonymous():
        profil = user.get_profile()
        produit_panier = Produit_Panier.objects.filter(panier=profil.panier_id)
        for p in produit_panier:
            prix += p.produit.prix * p.quantite
        article = produit_panier.count()
        menu_panier = profil.panier.menu_set.all()
        for m in menu_panier:
            prix+=m.typeMenu.prix
        article+= menu_panier.count()
        decimal=str(prix%1).split(".")[1]
    else:
        article = 0
    return { 'article':article, 'prix_panier':prix, 'decimal':decimal }

def publicites(request):
    sample_size = 3
    list = Produit.objects.all().order_by('?')[:sample_size]

    for p in list:
        p.decimal=str(p.prix%1).split(".")[1]
    return { 'publicites_produit': list }

def admin_media_prefix(request):
    return {'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX }
