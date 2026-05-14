from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import messages
from basdut_adventure.db import get_connection

import uuid

def login_user(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      
      # Pure SQL Query
      with get_connection().cursor() as cur:
         cur.execute(
            """
            SELECT UA.user_id, UA.username, UA.password, R.role_name
            FROM User_Account as UA
            JOIN Account_Role as AR ON UA.user_id = AR.user_id
            JOIN Role as R ON AR.role_id = R.role_id
            WHERE UA.username = %s
            """, 
            [username]
         )
         row = cur.fetchone()
         
      if row:
         user_id, db_username, db_password, db_role = row

         if password == db_password:
            # masukan data di session
            request.session['user_id'] = str(user_id) 
            request.session['username'] = db_username
            request.session['role'] = db_role
            request.session['is_authenticated'] = True 
            
            return redirect('main:mantap')
         else:
            messages.error(request, "Invalid password")
      else:
         messages.error(request, "User does not exist.")
         
   return render(request, 'login.html')

def logout_user(request):
   request.session.flush()
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
            messages.success(request, 'Your account has been successfully created!')
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
            messages.success(request, 'Your account has been successfully created!')
            conn.close()
         
        
   return redirect('autentikasi:login')