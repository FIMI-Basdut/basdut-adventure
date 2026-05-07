from django.shortcuts import render, redirect


def show_mantap(request):
    return render(request, "mantap.html")

def preview_navbar_guest(request):
    return render(request, 'base.html')

def preview_navbar_admin(request):
    context = {
        'role': 'admin',
        'username': 'Administrator'
    }
    return render(request, 'base.html', context)

def preview_navbar_organizer(request):
    context = {
        'role': 'organizer',
        'username': 'Andi Organizer'
    }
    return render(request, 'base.html', context)

def preview_navbar_customer(request):
    context = {
        'role': 'customer',
        'username': 'Izzudin Abdul Rasyid'
    }
    return render(request, 'base.html', context)