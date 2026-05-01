from django.shortcuts import render, redirect

def show_venue_list(request):
    return render(request, "venue_list_page.html")