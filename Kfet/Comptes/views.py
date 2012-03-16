from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from Kfet.Commun.models import Produit, Categorie
from django.template import RequestContext
from django.http import HttpResponse


def creation(request):
    return render_to_response('Comptes/creation.html' , context_instance=RequestContext(request))
