from Kfet.Commun.models import Categorie
from Kfet.Commun.models import Produit, Produit_Panier
from django.conf import settings


def categories(request):
    list = Categorie.objects.all()
    return { 'categories_list': list }

def articles(request):
    user = request.user
    if not user.is_anonymous():
        profil = user.get_profile()
        article = Produit_Panier.objects.filter(panier=profil.panier_id).count()
        article+= profil.panier.menus.count()
    else:
        article = 0
    return { 'article':article }

def publicites(request):
    sample_size = 3
    list = Produit.objects.all().order_by('?')[:sample_size]

    for p in list:
        p.decimal=str(p.prix%1).split(".")[1]
    return { 'publicites_produit': list }

def admin_media_prefix(request):
    return {'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX }
