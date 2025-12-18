from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    # Public URLs (tanpa login)
    path('', views.feedback_form, name='form'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
