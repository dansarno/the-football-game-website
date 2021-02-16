from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from enter import models
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response


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


def get_data(request):
    data = {
        'sales': 100,
        'customers': 10,
    }
    return JsonResponse(data)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        entry = models.Entry.objects.all()[2]  # filter(profile=request.user.profile)
        scorelog_qs = [scorelog['score'] for scorelog in entry.scorelog_set.values('score')]
        positionlog_qs = [positionlog['position'] for positionlog in entry.positionlog_set.values('position')]
        labels = [scorelog['called_bet__date'] for scorelog in entry.scorelog_set.values('called_bet__date')]

        data = {
            'id': entry.id,
            'current score': entry.current_score,
            'current position': entry.current_position,
            'scores': scorelog_qs,
            'positions': positionlog_qs,
            'labels': labels,
        }
        return Response(data)


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
