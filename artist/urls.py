from django.urls import include, path
from artist.views import show_daftar_artist, show_daftar_artist_admin

app_name = 'artist'

urlpatterns = [
    path('', show_daftar_artist, name='daftar_artist'),
    path('admin/', show_daftar_artist_admin, name='daftar_artist_admin'),
]