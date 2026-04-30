from django.urls import include, path
from ticket_category.views import show_tiket_kategori, show_tiket_kategori_admin

app_name = 'ticket_category'

urlpatterns = [
    path('', show_tiket_kategori, name='tiket_kategori'),
    path('admin/', show_tiket_kategori_admin, name='tiket_kategori_admin'),
]