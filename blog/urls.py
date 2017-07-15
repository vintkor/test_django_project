from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.all_posts, name="all_posts"),
    url(r'^(?P<post_id>[0-9]+)/$', views.single_post, name='blog_single_post')
]
