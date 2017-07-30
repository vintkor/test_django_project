from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.all_products, name="all_products"),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.single_post, name='catalog_single_product'),
    url(r'^category/(?P<cat_id>[0-9]+)/$', views.cat_products, name='catalog_category'),
]