from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserPasswordChangeForm, LoginForm, UserEditForm, ProfileEditForm, SubscribeForm, MassageForm
from django.contrib.auth import login, logout
from .models import Profile
from django.contrib.auth.decorators import login_required
from builder.models import Template, Languages
from django.utils.translation import gettext_lazy as _
from builder.context import get_context


def register(request):
    template = Template.objects.get(type='default', default=True).slug
    context = get_context()
    context['main'] = 'default_register.html'
    context['title'] = ''

    if request.method == 'POST':
        context['form'] = UserRegisterForm(request.POST)
        if context['form'].is_valid():
            new_user = context['form'].save()
            profile = Profile.objects.create(user=new_user)
            login(request, new_user, backend='account.authentication.EmailBackend')
            messages.success(request, _('You have successfully registered'))
            return redirect('account:profile')
        else:
            messages.error(request, _('Registration error'))
    else:
        context['form'] = UserRegisterForm()
    return render(request, template, context)


def user_login(request):
    template = Template.objects.get(type='default', default=True).slug
    context = get_context()
    context['main'] = 'default_login.html'
    context['title'] = ''

    if request.method == 'POST':
        context['form'] = UserLoginForm(data=request.POST)
        if context['form'].is_valid():
            user = context['form'].get_user()
            login(request, user)
            return redirect('account:profile')
    else:
        context['form'] = UserLoginForm()
    return render(request, template, context)


def user_logout(request):
    logout(request)
    return redirect('account:login')


def account(request):
    template = Template.objects.get(type='default', default=True).slug
    context = get_context()
    context['main'] = 'default_profile.html'
    context['title'] = ''
    return render(request, template, context)


def password_change(request):
    template = Template.objects.get(type='default', default=True).slug
    context = get_context()
    context['main'] = 'default_password_change.html'
    context['title'] = ''

    if request.method == 'POST':
        context['form'] = UserPasswordChangeForm(request.user, request.POST)
        if context['form'].is_valid():
            context['form'].save()
            messages.success(request, _('You have successfully changed your password'))
            return redirect('account')
        else:
            messages.error(request, _('Error'))
    else:
        context['form'] = UserPasswordChangeForm(request)
    return render(request, template, context)


@login_required
def edit(request):
    template = Template.objects.get(type='default', default=True).slug
    context = get_context()
    context['main'] = 'default_profile_edit.html'
    context['title'] = ''

    if request.method == 'POST':
        context['user_form'] = UserEditForm(instance=request.user, data=request.POST)
        context['profile_form'] = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if context['user_form'].is_valid() and context['profile_form'].is_valid():
            context['user_form'].save()
            context['profile_form'].save()
            messages.success(request, _('You have successfully made changes'))
        else:
            messages.error(request, _('Something went wrong'))
        return redirect('profile_edit')
    else:
        context['user_form'] = UserEditForm(instance=request.user)
        context['profile_form'] = ProfileEditForm(instance=request.user.profile)
        return render(request, template, context)


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your application has been accepted'))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, _('Subscription error, perhaps this email is already registered'))
        return redirect(request.META.get('HTTP_REFERER', '/'))


def message(request):
    if request.method == 'POST':
        form = MassageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your message has been sent'))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, _('Error, message not sent'))
        return redirect(request.META.get('HTTP_REFERER', '/'))


def lang(request):
    if request.method == 'POST':
        new_url = request.META['HTTP_REFERER']
        for item in Languages.objects.filter(status=True):
            if '/' + item.code + '/' in request.META['HTTP_REFERER']:
                new_url = request.META['HTTP_REFERER'].replace(item.code, 'my_lang_item')
        return redirect(new_url.replace('my_lang_item', request.POST['lang']))
