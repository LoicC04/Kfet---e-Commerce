from django.shortcuts import render_to_response
from django.template import RequestContext
from Kfet.Commun.models.Menu  import *
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    return render_to_response('Kfet/home.html', {}, context_instance=RequestContext(request) ) 

def listMenu(request):
    typeMenu = TypeMenu.objects.all()
    return render_to_response('Commandes/menus.html', {'typeMenu':typeMenu}, context_instance=RequestContext(request) ) 

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

