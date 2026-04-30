from django.shortcuts import render

# Create your views here.
def show_daftar_artist(request):
    return render(request, 'daftar_artis.html')
def show_daftar_artist_admin(request):
    return render(request, 'daftar_artis_admin.html')