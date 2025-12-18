from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.core.cache import cache
from .models import Feedback
from .forms import FeedbackForm


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def feedback_form(request):
    """Public view - Form feedback tanpa login dengan rate limiting"""
    # Get client IP
    client_ip = get_client_ip(request)
    cache_key = f'feedback_cooldown_{client_ip}'
    
    # Check if IP is in cooldown
    last_submit = cache.get(cache_key)
    
    if request.method == 'POST':
        if last_submit:
            # IP masih dalam cooldown
            remaining_time = last_submit
            messages.error(
                request, 
                f'Anda baru saja mengirim feedback. Silakan tunggu {remaining_time} menit sebelum mengirim lagi. ⏰'
            )
            form = FeedbackForm()
        else:
            # IP tidak dalam cooldown, process form
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()
                # Set cooldown untuk 20 menit
                cache.set(cache_key, 20, 20 * 60)  # 20 menit dalam detik
                return redirect('feedback:thank_you')
    else:
        form = FeedbackForm()
        # Tampilkan info jika masih cooldown
        if last_submit:
            messages.warning(
                request,
                f'Anda masih dalam periode cooldown. Tunggu {last_submit} menit untuk mengirim feedback lagi.'
            )
    
    return render(request, 'feedback/form.html', {'form': form})


def thank_you(request):
    """Public view - Thank you page setelah submit"""
    return render(request, 'feedback/thank_you.html')
