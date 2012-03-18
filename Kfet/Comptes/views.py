from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Promo, Personne
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError

def ajout(request):

    try: 
        etu_post = request.POST['etu']
    except MultiValueDictKeyError:
/bin/bash: :q : commande introuvable

    try: 
        nom_post = request.POST['nom']
    except MultiValueDictKeyError:
            nom_post = "FUCK"

    try: 
        prenom_post = request.POST['prenom']
    except MultiValueDictKeyError:
            prenom_post = "FUCK"

    try: 
        pass_post = request.POST['pass']
    except MultiValueDictKeyError:
            pass_post = "FUCK"

    try: 
        mail_post = request.POST['mail']
    except MultiValueDictKeyError:
            mail_post = "FUCK"

    try: 
        promo_post = request.POST['promo']
    except MultiValueDictKeyError:
            promo_post = 2

    personne = Personne(
        num_etu=etu_post,
        nom=nom_post,
        prenom=prenom_post,
        password=pass_post,
        mail=mail_post,
        promo_id=promo_post
    )
    personne.save()
    return HttpResponseRedirect(reverse('Kfet.Comptes.views.ok'))

def creation(request):
    promo = get_list_or_404(Promo)
    return render_to_response('Comptes/creation.html' , {'promo':promo}, context_instance=RequestContext(request))

def ok(request):
    return HttpResponse("Hey")
