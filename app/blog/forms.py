from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _


class ArticleShareEmailForm(forms.Form):
    name = forms.CharField(max_length=50, label=_('Name'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_from = forms.EmailField(max_length=150, label=_('Email from'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_to = forms.EmailField(max_length=150, label=_('Email to'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(required=False, label=_('Comments'), widget=forms.Textarea(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'class': 'form-control'})

