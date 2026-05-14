from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from basdut_adventure.db import get_connection

import uuid


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
      password = request.POST.get('password')
      user_id = str(uuid.uuid4())
      
      # get the tools for query in db
      conn = get_connection()
      
      if role == 'pelanggan':
         customer_id = str(uuid.uuid4())
         full_name = request.POST.get('nama')
         nomor_telepon = request.POST.get('nomor_telepon')
         
         try:
            with conn.cursor() as cur:
                  # get role id based on customer
                  cur.execute(
                     """
                     SELECT role_id
                     FROM ROLE
                     WHERE role_name = 'Customer'
                     """,
                  )
                  row = cur.fetchone()
                  
                  if row is None:
                     raise ValueError("Role not found")
                  
                  role_id = str(row[0])

                  # insert the user into user_account
                  cur.execute(
                     """
                     INSERT INTO USER_ACCOUNT (user_id, username, password)
                     VALUES (%s, %s, %s)
                     """,
                     (user_id, username, password),
                  )
                  
                  # insert the user and it's role into account_role
                  cur.execute(
                     """ 
                     INSERT INTO ACCOUNT_ROLE (role_id, user_id)
                     VALUES (%s, %s)
                     """,
                     (role_id, user_id)
                  )
                  
                  # insert the user into customer
                  cur.execute(
                     """ 
                     INSERT INTO CUSTOMER (customer_id, full_name, phone_number, user_id)
                     VALUES (%s, %s, %s, %s)
                     """,
                     (customer_id, full_name, nomor_telepon, user_id)
                  )
            conn.commit()
            
         except Exception:
            # If any query fails, undo everything
            conn.rollback()
            raise
         
         finally:
            conn.close()
         
      elif role == 'penyelenggara':
         organizer_id = str(uuid.uuid4())
         organizer_name = request.POST.get('nama_penyelenggara')
         email = request.POST.get('email')
         
         try:
            with conn.cursor() as cur:
                  # get role id based on organizer
                  cur.execute(
                     """
                     SELECT role_id
                     FROM ROLE
                     WHERE role_name = 'Organizer'
                     """,
                  )
                  row = cur.fetchone()
                  
                  if row is None:
                     raise ValueError("Role not found")
                  
                  role_id = str(row[0])

                  # insert the user into user_account
                  cur.execute(
                     """
                     INSERT INTO USER_ACCOUNT (user_id, username, password)
                     VALUES (%s, %s, %s)
                     """,
                     (user_id, username, password),
                  )
                  
                  # insert the user and it's role into account_role
                  cur.execute(
                     """ 
                     INSERT INTO ACCOUNT_ROLE
                     VALUES (%s, %s)
                     """,
                     (role_id, user_id)
                  )
                  
                  # insert the user into organizer
                  cur.execute(
                     """ 
                     INSERT INTO ORGANIZER
                     VALUES (%s, %s, %s, %s)
                     """,
                     (organizer_id, organizer_name, email, user_id)
                  )
            conn.commit()
            
         except Exception:
            # If any query fails, undo everything
            conn.rollback()
            raise
         
         finally:
            conn.close()
         
        
   return redirect('autentikasi:login')