from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'
urlpatterns = [
    path('about/', AboutView.as_view(), name='about_view'),
    path('causes/', CausesView.as_view(), name='causes_view'),
    path('contact/', ContactView.as_view(), name='contact_view'),
    path('donate/', DonateView.as_view(), name='donate_view'),
    path('event-single/<int:id>/', Event_Single_View.as_view(), name='event-single_view'),
    path('events/', EventView.as_view(), name='events_view'),
    path('event-single-gallery/<int:id>/', Event_Single_Gallery.as_view(), name='event-single-gallery_view'),
    path('events-gallery/', GalleryView.as_view(), name='events-gallery_view'),

    # making the indexview the ground-0 view of the site
    path('', IndexView.as_view(), name='home_view'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)