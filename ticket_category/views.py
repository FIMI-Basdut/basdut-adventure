from django.shortcuts import render

# Create your views here.

def show_tiket_kategori(request):
    return render(request, 'tiket_kategori.html')
def show_tiket_kategori_admin(request):
    return render(request, 'tiket_kategori_admin.html')