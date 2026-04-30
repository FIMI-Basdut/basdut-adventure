from django.urls import path
from .views import show_seat, dummy_seat_action

app_name = 'seat'

urlpatterns = [
    path('', show_seat, name='show_seat'),
    path('action/', dummy_seat_action, name='seat_action'),
]