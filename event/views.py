from django.shortcuts import render, redirect

def show_event_list(request):
    return render(request, "event_list_page.html")