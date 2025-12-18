from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['nama', 'umur', 'rating', 'kategori', 'komentar']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Anda (Opsional)'
            }),
            'umur': forms.Select(attrs={
                'class': 'form-select'
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'star-rating'
            }),
            'kategori': forms.Select(attrs={
                'class': 'form-select'
            }),
            'komentar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ceritakan pengalaman Anda...'
            }),
        }
