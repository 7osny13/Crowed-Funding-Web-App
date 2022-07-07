

from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect


@never_cache
def projectred(request):
    
    if request.method=='GET':

        return HttpResponseRedirect('/projects/projects_all')