from django.shortcuts import render, get_object_or_404
from blog.models import Post
from .forms import CommentForm
from testsite import settings
from django.views import View


def home(request):
    context = {"name": "Django", "theme": settings.SITE_THEME}
    return render(request, settings.SITE_THEME + '/base.html', context)


def all_posts(request):
    posts = Post.objects.all().order_by("-created")
    return render(request, settings.SITE_THEME + '/blog/blog_base.html', {"posts": posts})


def cat_posts(request, cat_id):
    posts = Post.objects.filter(post_category=cat_id).order_by("-created")
    return render(request, settings.SITE_THEME + '/blog/blog_base.html', {"posts": posts})


def single_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(initial={'comment_parent': post_id})
    context = {'post': post, 'form': form}
    if request.POST:
        f = CommentForm(request.POST)
        f.save()
    return render(request, settings.SITE_THEME + '/blog/single_post.html', context)


class Home(View):

    def get(self, request):
        context = {"name": "Django"}
        return render(request, settings.SITE_THEME + '/base.html', context)
