from django.shortcuts import render, get_object_or_404
from catalog.models import CatalogProduct
from testsite.settings import SITE_THEME


def all_products(request):
    products = CatalogProduct.objects.all().order_by('-created')
    print(products)
    context = {
        "products": products,
    }
    return render(request, SITE_THEME + '/catalog/list_view.html', context)


def single_post(request, product_id):
    context = {
        'product': get_object_or_404(CatalogProduct, pk=product_id),
        'images': CatalogProduct.get_all_images(product_id)
    }
    return render(request, SITE_THEME + '/catalog/single-product.html', context)
