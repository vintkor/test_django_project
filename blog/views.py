from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, Category, Comment


def home(request):
    context = {"name": "Django"}
    return render(request, 'base.html', context)


def all_posts(request):
    posts = Post.objects.all().order_by("-created")
    return render(request, 'blog/blog_base.html', {"posts": posts})


def single_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/single_post.html', {'post': post})
