from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.decorators import login_required
from enter import models


def landing(request):
    if request.user.is_authenticated:
        return redirect('feed:home')
    return render(request, 'feed/simple-landing.html', {
        'title': "Welcome",
    })


def charity(request):
    return render(request, 'feed/charity.html', {
        'title': "Charity",
    })


def how_it_works(request):
    return render(request, 'feed/how_it_works.html', {
        'title': "How It Works",
    })


def about(request):
    return render(request, 'feed/about.html', {
        'title': "About",
    })


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
