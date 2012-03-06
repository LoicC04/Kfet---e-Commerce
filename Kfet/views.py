from django.shortcuts import render_to_response, get_object_or_404

def home(request):
#    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('Kfet/home.html', {})
