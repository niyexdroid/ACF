from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<str:url_aware_title>/', PostDetailView.as_view(), name='post-detail'),

    # we may not necessarily need to implement a blog create page,
    # because then we have to validate using a LoginRequiredMixin on the view.
    # the admin can handle this, but we may still use it to make less people have access to the admin
    # though we may create certain permissions for their User instances.
    # path('create/', PostCreateView.as_view(), name='post-create'),
    # adding a path for the updateview
    # path('update/<int:id>/', PostUpdateView.as_view(), name='post-update'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
