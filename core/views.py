from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    """
    Handle user login
    GET: Tampilkan form login
    POST: Process login
    """
    # Redirect jika sudah login
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            
            # Redirect ke next URL atau dashboard
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:login')


@login_required
def dashboard_view(request):
    """
    Dashboard dengan akses berbeda berdasarkan role
    """
    user = request.user
    
    context = {
        'user': user,
        'role': user.get_role_display(),
    }
    
    # Tentukan akses berdasarkan role
    if user.role == 'GENERAL_MANAGER':
        context['accessible_apps'] = ['Customer', 'Pegawai', 'Logistik', 'Report']
        context['can_access_report'] = True
        context['can_access_logistik'] = True
        
    elif user.role == 'INVENTORY_MANAGER':
        context['accessible_apps'] = ['Customer', 'Pegawai', 'Logistik']
        context['can_access_report'] = False
        context['can_access_logistik'] = True
        
    else:  # EMPLOYEE
        context['accessible_apps'] = ['Customer', 'Pegawai']
        context['can_access_report'] = False
        context['can_access_logistik'] = False
    
    return render(request, 'core/dashboard.html', context)

