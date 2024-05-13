# views.py
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import CommentForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q



def search(request):
    query = request.GET.get('query', '')
    
    # Filter posts based on related fields using '__field__icontains' syntax
    posts = Post.published.filter(
        Q(title__icontains=query) |
        Q(categories__name__icontains=query) |  # Assuming 'name' is the field you want to search in the Category model
        Q(body__icontains=query) |
        Q(comments__message__icontains=query)  # Assuming 'message' is the field you want to search in the Comment model
    )
    
    
    return render(request, 'search.html', {'posts': posts, 'query': query})

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

#

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        print("Current Post:", post)  # Debugging print
        category = post.categories.first()
        print("Post Category:", category)
        other_posts = Post.published.filter(categories=category).exclude(pk=post.pk)[:5]  # Exclude the current post itself
        print("Other Posts:", other_posts)
        context['other_posts'] = other_posts
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            

            # Validate the data (modify as needed)
            if not (name and email and message):
                # Handle validation errors (e.g., display error messages in the template)
                return render(request, self.template_name, {'post': post, 'error': 'Please fill in all fields.'})

            # Create and save a new Comment object
            comment = Comment(post=post, name=name, email=email, message=message)
            comment.save()

            # Optional redirect to show the new comment (adjust URL pattern if needed)
            return redirect('post_detail', category=post.categories.first().slug, slug=post.slug)

        return render(request, self.template_name, {'post': post})
    
class PostAboutView(TemplateView):
    template_name = 'about.html'
    context_object_name = 'latest_posts'

    def get_queryset(self):
        categories = Category.objects.all()
        latest_posts = {}
        for category in categories:
            latest_post = Post.published.filter(categories=category).first()
            if latest_post:
                latest_posts[category] = latest_post
        return latest_posts

class PostContactView(TemplateView):
    template_name = 'contact.html'





