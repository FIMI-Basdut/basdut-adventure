from django.urls import path
from main.views import show_mantap, show_ticket

app_name = 'main'

urlpatterns = [
    path('', show_mantap, name='mantap'),
    path('tickets/', show_ticket, name='show_ticket')
]