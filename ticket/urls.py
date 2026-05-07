from django.urls import path
from .views import show_ticket,dummy_ticket_action

app_name = 'ticket'

urlpatterns = [
    path('', show_ticket, name='show_ticket'),
    path('action/', dummy_ticket_action, name='ticket_action'),
]