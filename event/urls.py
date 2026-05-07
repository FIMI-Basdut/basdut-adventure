from django.urls import path
from event.views import show_event_list

app_name = 'event'

urlpatterns = [
    path('', show_event_list, name='event_list'),
]