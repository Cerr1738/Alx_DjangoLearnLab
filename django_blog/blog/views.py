from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Post


# ----------------------------
# AUTHENTICATION VIEWS
# ----------------------------

def register(request):
    """Handles user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """Profile page (requires login)"""
    return render(request, "blog/profile.html")


# ----------------------------
# BLOG POST CRUD VIEWS
# ----------------------------

class PostListView(ListView):
    """Displays all blog posts"""
    model = Post
    template_name = "blog/post_list.html"   # Default: blog/post_list.html
    context_object_name = "posts"
    ordering = ["-published_date"]


class PostDetailView(DetailView):
    """Displays a single blog post"""
    model = Post
    template_name = "blog/post_detail.html"  # Default: blog/post_detail.html


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows logged-in users to create a new post"""
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # Set the author to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows authors to update their post"""
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Only the author can update
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows authors to delete their post"""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        # Only the author can delete
        post = self.get_object()
        return self.request.user == post.author
