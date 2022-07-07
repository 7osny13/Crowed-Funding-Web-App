from django.contrib import admin
from django.urls import include, path
from .views import *
from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
   # path('admin/', admin.site.urls),
    # path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),
     path('addo', add_project),
     path('projects_all', project_all),
     path('logout', logout),
     path('project_detail/<id>', project_detail),
     path('project_detail', project_det),
        path('rating/<id>', rating),
        path('comments/<id>', comment),
        path('comrpt/<id>',comment_report),
        path('prorpt/<id>',project_report),
        path('prodel/<id>',project_delete),
        path('prodon/<id>',project_donate),
        path('search',searching),
        path('filter',project_filter_by_cat)
 ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'projects.views.error_404'
handler500 = 'projects.views.error_500'