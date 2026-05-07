from django.urls import path
from .views import show_order_list, show_order_create, dummy_order_action

app_name = 'order'

urlpatterns = [
    path('', show_order_list, name='show_order_list'),
    path('create/', show_order_create, name='show_order_create'),
    path('action/', dummy_order_action, name='order_action')
]
