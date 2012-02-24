# -*- coding: utf-8 -*-
from tuto.polls.models import Poll
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('polls/index.html')
    c = Context({
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

def detail(request, poll_id):
    return HttpResponse("Vous êtes bien au sondage numéro {}.".format(poll_id)) 
