# Create your views here.
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Kfet.Commun.models import Status_Commande, Commande




@user_passes_test(lambda u: u.is_staff)
def index(request):
    context={}
    context["nb_en_attente"] = Status_Commande.objects.get(code=1).commande_set.count()
    context["nb_en_cours"] = Status_Commande.objects.get(code=2).commande_set.count()
    context["nb_terminee"] = Status_Commande.objects.get(code=3).commande_set.count()
    context["nb_annulee"] = Status_Commande.objects.get(code=-1).commande_set.count()

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

    return render_to_response('GestionCommandes/list_commande.html', context, context_instance=RequestContext(request))

