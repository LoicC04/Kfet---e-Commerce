# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Promo, Personne
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError


def ajout(request):

    try:
        request.session['etu'] = request.POST['etu']
    except MultiValueDictKeyError:
        request.session['etu'] = ""
    try:
        request.session['nom'] = request.POST['nom']
    except MultiValueDictKeyError:
        request.session['nom'] = ""
    try:
        request.session['prenom'] = request.POST['prenom']
    except MultiValueDictKeyError:
        request.session['prenom'] = ""
    try:
        request.session['mail'] = request.POST['mail']
    except MultiValueDictKeyError:
        request.session['mail'] = ""

    if request.POST['nom'] == "":
        return HttpResponseRedirect('/comptes/creation/1')
    else:
        nom_post = request.POST['nom']

    if request.POST['etu'] == "":
        return HttpResponseRedirect('/comptes/creation/3')
    else:
        etu_post = request.POST['etu']

    if request.POST['prenom'] == "":
        return HttpResponseRedirect('/comptes/creation/2')
    else:
        prenom_post = request.POST['prenom']

    if request.POST['mail'] == "":
        return HttpResponseRedirect('/comptes/creation/4')
    else:
        mail_post = request.POST['mail']

    if request.POST['promo'] == "":
        return HttpResponseRedirect('/comptes/creation/5')
    else:
        promo_post = request.POST['promo']

    pass_post = request.POST['pass']


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

def creation(request,erreur):
    if 'etu' in request.session:
        etu_post = request.session['etu']
    else:
        etu_post = ""
    if 'nom' in request.session:
        nom_post = request.session['nom']
    else:
        nom_post = ""
    if 'prenom' in request.session:
        prenom_post = request.session['prenom']
    else:
        prenom_post = ""
    pass_post = ""
    if 'mail' in request.session:
        mail_post = request.session['mail']
    else:
        mail_post = ""
    if 'promo' in request.session:
        promo_post = request.session['promo']
    else:
        promo_post = ""

    personne = Personne(
        num_etu=etu_post,
        nom=nom_post,
        prenom=prenom_post,
        password=pass_post,
        mail=mail_post,
        promo_id=promo_post
    )

    promo = get_list_or_404(Promo)
    return render_to_response('Comptes/creation.html' , {'promo':promo, 'personne':personne, 'erreur':erreur}, context_instance=RequestContext(request))

def ok(request):

    try:
        del request.session['etu']
    except KeyError:
        pass
    try:
        del request.session['nom']
    except KeyError:
        pass   
    try:
        del request.session['prenom']
    except KeyError:
        pass
    try:
        del request.session['mail']
    except KeyError:
        pass
    return HttpResponse("Hey")

def test(request):
        if 'count' in request.session:
            request.session['count'] += 1
            return HttpResponse('new count=%s' % request.session['count'])
        else:
            request.session['count'] = 1
            return HttpResponse('No count in session. Setting to 1')
