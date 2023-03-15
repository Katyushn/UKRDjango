from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile, Subscribe, Message
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Name'), help_text=_('Maximum 150 characters'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label=_('New password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):  # arbitrary validation of the form before sending
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(_("The user with this email is not registered."))
        return email

    class Meta:
        model = User
        fields = ('email',)


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label=_('Name'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Surname'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(label=_('Birthday'), widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ('email',)


class MassageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('email', 'name', 'message')

