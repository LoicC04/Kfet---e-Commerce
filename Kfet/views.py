from django.shortcuts import render_to_response
from django.template import RequestContext
from Kfet.Commun.models  import TypeMenu, Produit, TypeMenu
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
        category = request.POST['category']
        produit = Produit.objects.filter(nom__contains=keyword)
        menu = TypeMenu.objects.filter(nom__contains=keyword)
    return render_to_response('recherche.html', {'produit':produit, 'menu':menu}, context_instance=RequestContext(request) )

