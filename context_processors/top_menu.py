from django.template.context_processors import request
from django.contrib import auth
from blog.models import Category


def user(request):
    user = auth.get_user(request)
    context = {'user': user}
    return context


def categories(request):
    categories = Category.objects.all()
    context = {'nodes': categories}
    return context