from django import forms
from .models import Comment

class AddCommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Поделитесь вашим мнением о книге'
        }),
        label='Ваш комментарий',
        required=True
    )