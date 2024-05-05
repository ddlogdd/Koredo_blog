# views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm
from django.urls import reverse

class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'latest_posts'

    def get_queryset(self):
        categories = Category.objects.all()
        latest_posts = {}
        for category in categories:
            latest_post = Post.published.filter(categories=category).first()
            if latest_post:
                latest_posts[category] = latest_post
        return latest_posts

class PostListView(ListView):
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category'])
        return Post.published.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', category=post.categories.first().slug, slug=post.slug)
        return render(request, self.template_name, {'post': post, 'form': form})
