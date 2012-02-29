# -*- coding: utf-8 -*-
from tuto.polls.models import Choice,Poll
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tuto.polls.models import Choice, Poll

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list':
latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p})

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})

#@csrf_exempt
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Réafficher le formulaire de vote du sondage.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "Veuillez sélectionner une réponse.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Toujours renvoyer une HttpResponseRedirect après avoir
        # correctement traité les données POST. Cela empêche de poster les
        # données deux fois si l'utilisateur appuie sur le bouton
        # "précedent".
        return HttpResponseRedirect(reverse('tuto.polls.views.results', args=(p.id,)))

