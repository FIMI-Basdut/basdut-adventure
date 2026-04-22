from django.urls import path
from main.views import show_mantap

app_name = 'main'

urlpatterns = [
    path('', show_mantap, name='mantap'),
]