from django.urls import path
from main.views import show_mantap,preview_navbar_admin,preview_navbar_customer,preview_navbar_guest,preview_navbar_organizer


app_name = 'main'

urlpatterns = [
    path('', show_mantap, name='mantap'),
    path('navbar/guest', preview_navbar_guest, name='nav_guest'),
    path('navbar/admin', preview_navbar_admin, name='nav_admin'),
    path('navbar/organizer', preview_navbar_organizer, name='nav_organizer'),
    path('navbar/customer', preview_navbar_customer, name='nav_customer'),
]