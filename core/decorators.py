from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    """
    Decorator untuk check role user
    
    Usage:
        @role_required(['GENERAL_MANAGER'])
        def some_view(request):
            ...
        
        @role_required(['INVENTORY_MANAGER', 'GENERAL_MANAGER'])
        def another_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check jika user punya role yang diizinkan
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # Jika tidak punya akses - redirect ke dashboard dengan pesan error
            messages.error(request, f'Access Denied! You need {" or ".join(allowed_roles)} role to access this page.')
            return redirect('core:dashboard')
        
        return wrapper
    return decorator
