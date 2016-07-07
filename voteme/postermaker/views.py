from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def poster(request):
    return render_to_response('postermaker/poster.html', {
        }, context_instance=RequestContext(request))
