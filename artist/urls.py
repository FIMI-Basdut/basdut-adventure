from django.urls import path
from . import views

app_name = 'artist' 

urlpatterns = [
    # URL Publik / Non-Admin
    path('/', views.daftar_artis, name='daftar_artis'),

    # URL Khusus Admin
    path('admin/', views.daftar_artis_admin, name='daftar_artis_admin'),
    path('admin/edit/<uuid:id>/', views.edit_artis, name='edit_artis'),
    path('admin/hapus/<uuid:id>/', views.hapus_artis, name='hapus_artis'),
]