from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.show_cart, name="show_cart"),
    url(r'^delete/(?P<item_id>[0-9]+)/$', views.delete_item, name="delete_item"),
]
