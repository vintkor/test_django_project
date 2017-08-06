from django.conf.urls import url
from . import views
from .views import Home


urlpatterns = [
    url(r'^$', Home.as_view(), name="all_posts"),
    url(r'^(?P<post_id>[0-9]+)/$', views.single_post, name='blog_single_post'),
    url(r'^category/(?P<cat_id>[0-9]+)/$', views.cat_posts, name='blog_cat_post'),
]
