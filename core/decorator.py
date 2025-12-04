from functools import wraps
from django.shortcuts import redirect

def role_required(allowed_roles=[]):
    """Decorator untuk membatasi akses berdasarkan peran pengguna"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('denied')  
            else:
                return redirect('login')  
        return _wrapped_view
    return decorator