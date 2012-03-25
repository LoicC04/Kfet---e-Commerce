from Kfet.Commun.models import Categorie
from Kfet.Commun.models import Produit
from random import sample


def categories(request):
    list = Categorie.objects.all()
    return { 'categories_list': list }

def publicites(request):
    count = Produit.objects.all().count()
    if count>=3:
        sample_size=3
        rand_ids = sample(xrange(1, count+1), sample_size)
        list = Produit.objects.filter(id__in=rand_ids)
    elif count==0:
        return {}
    else:
        list = Produit.objects.all()

    for p in list:
        p.decimal=str(p.prix%1).split(".")[1]
    return { 'publicites_produit': list }
