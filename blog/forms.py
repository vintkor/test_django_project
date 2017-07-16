from django import forms
from django.forms import HiddenInput, Textarea
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text", "comment_parent"]
        widgets = {
            'comment_parent': HiddenInput(),
            'comment_text': Textarea(attrs={'class': 'form-control', 'rows': '5', 'cols': ''})
        }

