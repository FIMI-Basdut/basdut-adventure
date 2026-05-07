from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Artist

# VIEWS UNTUK NON-ADMIN (R - Artist)
def daftar_artis(request):
    artists = Artist.objects.all()
    total_genre = Artist.objects.exclude(genre__isnull=True).exclude(genre__exact='').values('genre').distinct().count()
    context = {
        'artists': artists,
        'total_artis': artists.count(),
        'total_genre': total_genre,
    }
    return render(request, 'daftar_artis.html', context)


# VIEWS UNTUK ADMIN (CRUD - Artist)
def daftar_artis_admin(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        genre = request.POST.get('genre', '').strip()

        if not name:
            messages.error(request, 'Nama wajib diisi.')
        else:
            Artist.objects.create(name=name, genre=genre)
            messages.success(request, 'Daftar artis diperbarui.')
        
        return redirect('artist:daftar_artis_admin') 

    artists = Artist.objects.all()
    total_genre = Artist.objects.exclude(genre__isnull=True).exclude(genre__exact='').values('genre').distinct().count()
    context = {
        'artists': artists,
        'total_artis': artists.count(),
        'total_genre': total_genre,
    }
    return render(request, 'daftar_artis_admin.html', context)

def edit_artis(request, id):
    if request.method == 'POST':
        artist = get_object_or_404(Artist, id=id)
        name = request.POST.get('name', '').strip()
        genre = request.POST.get('genre', '').strip()

        if not name:
            messages.error(request, 'Nama wajib diisi.')
        else:
            artist.name = name
            artist.genre = genre
            artist.save()
            messages.success(request, 'Daftar artis diperbarui.')
            
    return redirect('artist:daftar_artis_admin')

def hapus_artis(request, id):
    if request.method == 'POST':
        artist = get_object_or_404(Artist, id=id)
        artist.delete()
        messages.success(request, 'Artis berhasil dihapus.')
        
    return redirect('artist:daftar_artis_admin')