from django.urls import path
from event.views import show_event_list, add_event

app_name = 'event'

urlpatterns = [
    path('', show_event_list, name='event_list'),
    path('add-event/', add_event, name='add_event'),
]