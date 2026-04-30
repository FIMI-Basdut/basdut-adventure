from django.shortcuts import render, redirect




def show_mantap(request):
    return render(request, "mantap.html")

def show_ticket(request):
    return render(request, 'ticket.html')