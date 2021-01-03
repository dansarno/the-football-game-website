from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has now been created! You are now able to log in")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'title': "Register",
        'form': form
    })


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {
        'title': user.username,
        'user': user
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
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile_edit.html', {
        'title': f"edit {request.user.username}",
        'u_form': u_form,
        'p_form': p_form
    })
