from django.shortcuts import render

# Create your views here.

def dashboard(request):
    data = {
        'total_user': 2543,
        'total_event': 156,
        'revenue': 'Rp 52.4M',
        'promo': 3,

        'venue_total': '3 Lokasi',
        'reserved': '2 Venue',
        'kapasitas': '1000 Kursi',

        'promo_percent': '1 Aktif',
        'promo_nominal': '1 Aktif',
        'total_used': '57 Kali'
    }

    return render(request, 'cek.html', data)