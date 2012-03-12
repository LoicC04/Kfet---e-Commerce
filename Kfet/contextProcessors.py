from Kfet.Commun.models import Categorie

def categories(request):
    list = Categorie.objects.all()
    return { 'categories_list': list }
