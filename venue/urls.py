from django.urls import path
from venue.views import show_venue_list, add_venue, update_venue, delete_venue

app_name = 'venue'

urlpatterns = [
    path('', show_venue_list, name='venue_list'),
    path('add-venue/', add_venue, name='add_venue'),
    path('update-venue/<str:id>/', update_venue, name='update_venue'),
    path('delete-venue/<str:id>/', delete_venue, name='delete_venue'),
]