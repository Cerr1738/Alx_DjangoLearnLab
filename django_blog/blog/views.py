from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Post
from .forms import PostForm

# --- Search View ---
def post_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)  # search by tags
        ).distinct()
    return render(request, 'blog/post_search.html', {'results': results, 'query': query})

# --- Tag View ---
def post_by_tag(request, tag_name):
    results = Post.objects.filter(tags__name__iexact=tag_name)
    return render(request, 'blog/post_by_tag.html', {'results': results, 'tag': tag_name})

# --- Post Detail View ---
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

# --- Create Post View ---
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# --- Update Post View ---
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
