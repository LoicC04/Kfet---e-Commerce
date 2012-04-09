from django.shortcuts import render_to_response
from django.template import RequestContext
from Kfet.Commun.models  import TypeMenu
from django.contrib.auth.decorators import login_required


def home(request):
    return render_to_response('Kfet/home.html', {}, context_instance=RequestContext(request) ) 

def listMenu(request):
    typeMenu = TypeMenu.objects.filter(actif=True)
    return render_to_response('Commandes/menus.html', {'typeMenu':typeMenu}, context_instance=RequestContext(request) ) 

@login_required
def administration(request):
    return render_to_response('Kfet/administration.html', {}, context_instance=RequestContext(request) ) 
