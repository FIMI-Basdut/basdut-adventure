from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
       
        if not request.session.get('is_authenticated'):
            # Belom login, maka lemparkan ke page login
            return redirect('autentikasi:login') 
        
        # Sudah login, maka berikan page yang ditentukan
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view