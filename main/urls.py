from django.urls import include, path
from main.views import show_mantap
from dashboard.views import dashboard

app_name = 'main'

urlpatterns = [
    path('', show_mantap, name='mantap'),
    path('dashboard/', dashboard, name='dashboard'),
]