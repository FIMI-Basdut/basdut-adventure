from django.urls import path
from venue.views import show_venue_list

app_name = 'venue'

urlpatterns = [
    path('', show_venue_list, name='venue'),
]