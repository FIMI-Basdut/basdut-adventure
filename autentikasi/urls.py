from django.urls import path
from autentikasi.views import login_user, logout_user, register_action, register_form, register_role_selection

app_name = 'autentikasi'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    path('register/', register_role_selection, name='register_role_selection'),
    path('register/form/', register_form, name='register_form'),
    path('register/action/', register_action, name='register_action'),
]