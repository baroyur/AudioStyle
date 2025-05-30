from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'input-field'}),
            'text': forms.Textarea(attrs={'placeholder': 'Ваш комментарий', 'class': 'textarea-field', 'rows': 4}),
        }
