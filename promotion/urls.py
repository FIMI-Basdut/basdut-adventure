from django.urls import path
from .views import show_promotions, dummy_promo_action

app_name = 'promotion'

urlpatterns = [
    path('', show_promotions, name='show_promotions'),
    path('action/', dummy_promo_action, name='promo_action')
]
