from django.urls import path
from .views import show_seat, seat_action

app_name = 'seat'

urlpatterns = [
    path('', show_seat, name='show_seat'),
    path('action/', seat_action, name='seat_action'),
]