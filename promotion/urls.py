from django.urls import path
from .views import show_promotions, dummy_promo_action, create_promotion

app_name = 'promotion'

urlpatterns = [
    path('', show_promotions, name='show_promotions'),
    path('action/', dummy_promo_action, name='promo_action'),
    path('action/create', create_promotion, name='create_promo')
]
