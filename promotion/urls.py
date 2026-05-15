from django.urls import path
from .views import show_promotions, dummy_promo_action, create_promotion, delete_promotion, update_promotion

app_name = 'promotion'

urlpatterns = [
    path('', show_promotions, name='show_promotions'),
    path('action/', dummy_promo_action, name='promo_action'),
    path('action/create', create_promotion, name='create_promo'),
    path('action/delete', delete_promotion, name='delete_promo'),
    path('action/update', update_promotion, name='update_promo'),
]
