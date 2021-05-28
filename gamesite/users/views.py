from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, AccessCode
from enter import models
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_profile = new_user.profile
            access_code = user_form.cleaned_data.get('access_code')
            access_code_obj = AccessCode.objects.filter(code=access_code).first()
            access_code_obj.remaining -= 1
            access_code_obj.save()
            new_profile.access_code = access_code_obj
            new_profile.save()
            messages.success(request, f"Your account has now been created! You are now able to log in")
            return redirect('login')
    else:
        user_form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'title': "Register",
        'user_form': user_form
    })


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    entries = user.profile.entries.filter(has_submitted=True)

    return render(request, 'users/profile.html', {
        'title': user.username,
        'user': user,
        'entries': entries,
        'team': user.profile.team,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated")
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile_edit.html', {
        'title': f"edit {request.user.username}",
        'u_form': u_form,
        'p_form': p_form
    })
