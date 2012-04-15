from django.shortcuts import render_to_response
from django.template import RequestContext
from Kfet.Commun.models  import TypeMenu, Produit, TypeMenu, Categorie
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home(request):
    return render_to_response('Kfet/home.html', {}, context_instance=RequestContext(request) ) 

def listMenu(request):
    typeMenu = TypeMenu.objects.filter(actif=True)
    return render_to_response('Commandes/menus.html', {'typeMenu':typeMenu}, context_instance=RequestContext(request) ) 

def recherche(request):    
    if request.method == 'POST':
        keyword = request.POST['keyword']
        keywords = keyword.split(' ') 
        category = request.POST['category']                

        if category == "default":
            if len(keywords) == 1:
                produit = Produit.objects.filter(nom__icontains=keywords[0])
            else:
                produit = []
                for key in keywords:
                    test = 0
                    pro = Produit.objects.filter(nom__icontains=key)
                    for result in produit:
                        try:
                            if result == pro[0]:
                                test = 1
                        except IndexError:
                            pass
                    if test == 0:
                        produit += pro
        else:
            categorie = Categorie.objects.get(nom=category)
            produit = Produit.objects.filter(nom__icontains=keyword, categorie=categorie.id)
        menu = TypeMenu.objects.filter(nom__icontains=keyword)
    return render_to_response('recherche.html', {'produit':produit, 'menu':menu, 'keyword':keyword, 'category':category}, context_instance=RequestContext(request) )

