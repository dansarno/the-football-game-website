from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.http import HttpResponse
import csv


def landing(request):
    if request.user.is_authenticated:
        return redirect('feed:home')
    return render(request, 'feed/very-simple-landing.html', {
        'title': "Welcome",
    })


@login_required
def charity(request):
    return render(request, 'feed/charity.html', {
        'title': "Charity",
    })


@login_required
def entry_guide(request):
    return render(request, 'feed/guide.html', {
        'title': "Entry Guide",
    })


@login_required
def entry_guide_italian(request):
    return render(request, 'feed/guide_IT.html', {
        'title': "Come Giocare",
    })


@login_required
def glossary(request):
    return render(request, 'feed/glossary.html', {
        'title': "Glossario",
    })


@login_required
def how_it_works(request):
    return render(request, 'feed/how_it_works.html', {
        'title': "How It Works",
    })


@login_required
def how_it_works_italian(request):
    return render(request, 'feed/how_it_works_IT.html', {
        'title': "Come Funziona",
    })


@login_required
def about(request):
    return render(request, 'feed/about.html', {
        'title': "About",
    })


def export_csv(request):
    if not request.user.is_superuser:
        return redirect('feed:home')

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['', '', '', '', '', 'Entry A', '', 'Entry B', '', 'Entry C', ''])
    writer.writerow(['First name', 'Last name', 'Username', 'Access Code Used', 'Email Address', 'Created?', 'Submitted?', 'Created?', 'Submitted?', 'Created?', 'Submitted?'])

    for profile in Profile.objects.all():
        first_name = profile.user.first_name
        last_name = profile.user.last_name
        username = profile.user.username
        if profile.access_code:
            access_code = profile.access_code.code
        else: 
            access_code = None
        email_address = profile.user.email
        entry_info = [False] * 6
        for i, entry in enumerate(profile.entries.all()):
            entry_info[i * 2] = True
            entry_info[(i * 2) + 1] = entry.has_submitted
        writer.writerow([first_name, last_name, username, access_code, email_address] + entry_info)

    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    return response


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView,self).get_context_data(*args, **kwargs)
        context['pinned_post'] = Post.objects.order_by('-date_posted').filter(is_pinned=True).first()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
