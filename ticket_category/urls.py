from django.urls import path
from . import views

app_name = 'ticket_category'

urlpatterns = [
    # URL Publik / Non-Admin
    path('', views.daftar_tiket_kategori, name='daftar_tiket_kategori'),
    
    # URL Khusus Admin
    path('admin/', views.daftar_tiket_kategori_admin, name='daftar_tiket_kategori_admin'),
    path('admin/edit/<uuid:id>/', views.edit_tiket_kategori, name='edit_tiket_kategori'),
    path('admin/hapus/<uuid:id>/', views.hapus_tiket_kategori, name='hapus_tiket_kategori'),
]