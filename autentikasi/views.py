from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:mantap')

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
   logout(request)
   return redirect('autentikasi:login')

def register_role_selection(request):
   return render(request, 'register.html')

def register_form(request):
   role = request.GET.get('role')

   valid_roles = ['pelanggan', 'penyelenggara', 'administrator']
   if role not in valid_roles:
      return redirect('autentikasi:register_role_selection')

   context = {
      'role': role
   }
   return render(request, 'register_form.html', context)

def register_action(request):
   if request.method == "POST":
      role = request.POST.get('role')
      username = request.POST.get('username')
        
   return redirect('autentikasi:login')