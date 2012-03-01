from django.http import HttpResponse
from tuto.polls.models import Poll

def index(request):
    p = Poll.objects.get(pk=1)
    return HttpResponse("Hello, world. You're at the Stock index. {}".format(p.question))
