from django.shortcuts import render, redirect


def show_mantap(request):
    return render(request, "mantap.html")

