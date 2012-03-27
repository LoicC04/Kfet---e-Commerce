from Kfet.Commun.models import Categorie
from Kfet.Commun.models import Produit
from django.conf import settings


def categories(request):
    list = Categorie.objects.all()
    return { 'categories_list': list }

def publicites(request):
    sample_size = 3
    list = Produit.objects.all().order_by('?')[:sample_size]

    for p in list:
        p.decimal=str(p.prix%1).split(".")[1]
    return { 'publicites_produit': list }

def admin_media_prefix(request):
    return {'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX } 
