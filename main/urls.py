from django.urls import path
from main.views import show_mantap, show_ticket, show_seat,dummy_seat_action

app_name = 'main'

urlpatterns = [
    path('', show_mantap, name='mantap'),
    path('tickets/', show_ticket, name='show_ticket'),
    path('seats/', show_seat, name='show_seat'),
    path('seats/action/', dummy_seat_action, name='seat_action'),
]