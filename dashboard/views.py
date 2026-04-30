from django.shortcuts import render

# Create your views here.

def show_dashboard_customer(request):
    return render(request, 'dashboard_customer.html')
def show_dashboard_organizer(request):
    return render(request, 'dashboard_organizer.html')
def show_dashboard_admin(request):
    return render(request, 'dashboard_admin.html')
def show_profile_customer(request):
    return render(request, 'profile_customer.html')
def show_profile_organizer(request):
    return render(request, 'profile_organizer.html')