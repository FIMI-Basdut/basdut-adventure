from django.urls import path
from autentikasi.views import login_user, logout_user

app_name = 'autentikasi'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]