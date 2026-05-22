from django.urls import path
from .views import show_order_list, show_order_create, dummy_order_action, update_order, delete_order

app_name = 'order'

urlpatterns = [
    path('', show_order_list, name='show_order_list'),
    path('create/<str:event_id>/', show_order_create, name='show_order_create'),
    path('action/', dummy_order_action, name='order_action'),
    path('action/update', update_order, name='update_order'),
    path('action/delete', delete_order, name='delete_order')
]
