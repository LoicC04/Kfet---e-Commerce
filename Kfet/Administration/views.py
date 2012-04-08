from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from Kfet.Commun.models.TypeMenu import TypeMenu, TypeMenuForm
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse


@login_required
def index(request):
    return render_to_response('Administration/index.html', { }, context_instance=RequestContext(request))

@login_required
def typeMenu(request):
    menus = TypeMenu.objects.all()
    return render_to_response('Administration/typeMenu.html', { 'menus':menus }, context_instance=RequestContext(request))

@login_required
def ajouterModifierMenu(request, menu_id=None):
    if menu_id!=None:
        menu = get_object_or_404(TypeMenu, pk=menu_id)
    else:
        menu = TypeMenu()
    
    if request.method=='POST':
        form = TypeMenuForm(data=request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('Kfet.Administration.views.typeMenu'))
    else:
        form = TypeMenuForm(instance=menu)
    return render_to_response('Administration/ajouterModifierMenu.html', {'form':form , 'menu_id':menu_id}, context_instance=RequestContext(request))

@login_required
def typePaiement(request):
    return render_to_response('Administration/typePaiement.html', { }, context_instance=RequestContext(request))

@login_required
def dettes(request):
    return render_to_response('Administration/dettes.html', { }, context_instance=RequestContext(request))
