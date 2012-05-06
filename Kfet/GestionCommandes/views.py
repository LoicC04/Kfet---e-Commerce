# Create your views here.
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Kfet.Commun.models import Status_Commande, Commande
from django import forms



class Status_CommandeForm(forms.Form):
    status_commande = forms.ModelChoiceField(Status_Commande.objects.all())

@user_passes_test(lambda u: u.is_staff)
def index(request):
    context={}
    context["nb_en_attente"] = get_object_or_404(Status_Commande, code=1).commande_set.count()
    context["nb_en_cours"] = get_object_or_404(Status_Commande, code=2).commande_set.count()
    context["nb_terminee"] = get_object_or_404(Status_Commande, code=3).commande_set.count()
    context["nb_annulee"] = get_object_or_404(Status_Commande, code=-1).commande_set.count()

    return render_to_response('GestionCommandes/index.html', context, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def listCommande(request, statut=1):
    context={}
    statut=int(statut)
    statut_en_attente = get_object_or_404(Status_Commande, code=statut)

    en_attente_list = statut_en_attente.commande_set.all()
    paginator = Paginator(en_attente_list, 10) # Show 10 items per page
    page = request.GET.get('page',1)
    try:
        en_attente = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        en_attente = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        en_attente = paginator.page(paginator.num_pages)
    context["en_attente"]=en_attente

    context["form"]=Status_CommandeForm()

    return render_to_response('GestionCommandes/list_commande.html', context, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def changerEtatCommande(request, num_commande):

    num_commande = int(num_commande)
    commande = get_object_or_404(Commande, id=num_commande)

    if request.method=='POST':
        form = Status_CommandeForm(request.POST)
        if form.is_valid():
            code_status = int(form.cleaned_data["status_commande"].code)
            status = get_object_or_404(Status_Commande, code=code_status)
            commande.status_commande = status
            commande.save()
            return listCommande(request, statut=status.code)
    else:
        return listCommande(request)


@user_passes_test(lambda u: u.is_staff)
def annuler(request, num_commande):

    num_commande = int(num_commande)
    commande = get_object_or_404(Commande, id=num_commande)

    status = get_object_or_404(Status_Commande, code=-1)

    commande.status_commande = status
    commande.save()

    return listCommande(request, statut=status.code)
