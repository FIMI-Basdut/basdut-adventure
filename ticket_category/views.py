from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Max
from .models import TicketCategory
#from event.models import Event

# VIEWS UNTUK NON-ADMIN (R - TicketCategory)
def daftar_tiket_kategori(request):
    categories = TicketCategory.objects.all()
    context = {
        'categories': categories,
        'total_categories': categories.count(),
        'total_quota': categories.aggregate(Sum('quota'))['quota__sum'] or 0,
        'highest_price': categories.aggregate(Max('price'))['price__max'] or 0,
    }
    return render(request, 'tiket_kategori.html', context)

# VIEWS UNTUK ADMIN (CRUD - TicketCategory)
def daftar_tiket_kategori_admin(request):
    if request.method == 'POST':
        #event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name', '').strip()
        category_name = request.POST.get('category_name', '').strip()
        quota = request.POST.get('quota')
        price = request.POST.get('price')

        #if not all([event_id, category_name, quota, price]):
        if not all([event_name, category_name, quota, price]):
            messages.error(request, 'Semua input wajib diisi!')
        elif int(quota) <= 0:
            messages.error(request, 'Kuota harus lebih dari 0.')
        elif float(price) < 0:
            messages.error(request, 'Harga tidak boleh negatif.')
        else:
            #event = get_object_or_404(Event, id=event_id)
            #TicketCategory.objects.create(
            #    event=event, category_name=category_name, quota=quota, price=price
            #)
            TicketCategory.objects.create(
                event_name=event_name, category_name=category_name, quota=quota, price=price
            )
            messages.success(request, 'Kategori tiket berhasil ditambahkan.')
        
        return redirect('ticket_category:daftar_tiket_kategori_admin')

    categories = TicketCategory.objects.all()
    #events = Event.objects.all()
    
    context = {
        'categories': categories,
        #'events': events,
        'total_categories': categories.count(),
        'total_quota': categories.aggregate(Sum('quota'))['quota__sum'] or 0,
        'highest_price': categories.aggregate(Max('price'))['price__max'] or 0,
    }
    return render(request, 'tiket_kategori_admin.html', context)

def edit_tiket_kategori(request, id):
    if request.method == 'POST':
        category = get_object_or_404(TicketCategory, id=id)
        #event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name', '').strip()
        category_name = request.POST.get('category_name', '').strip()
        quota = request.POST.get('quota')
        price = request.POST.get('price')

        #if not all([event_id, category_name, quota, price]):
        if not all([event_name, category_name, quota, price]):
            messages.error(request, 'Semua input wajib diisi!')
        elif int(quota) <= 0:
            messages.error(request, 'Kuota harus lebih dari 0.')
        elif float(price) < 0:
            messages.error(request, 'Harga tidak boleh negatif.')
        else:
            #event = get_object_or_404(Event, id=event_id)
            #category.event = event
            category.event_name = event_name
            category.category_name = category_name
            category.quota = quota
            category.price = price
            category.save()
            messages.success(request, 'Kategori tiket berhasil diperbarui.')

    return redirect('ticket_category:daftar_tiket_kategori_admin')

def hapus_tiket_kategori(request, id):
    if request.method == 'POST':
        category = get_object_or_404(TicketCategory, id=id)
        category.delete()
        messages.success(request, 'Kategori tiket berhasil dihapus.')
    return redirect('ticket_category:daftar_tiket_kategori_admin')