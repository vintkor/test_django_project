from django.shortcuts import render, get_object_or_404
from catalog.models import CatalogProduct
from testsite.settings import SITE_THEME
from cart.models import Cart, Item
from django.utils.crypto import get_random_string


def all_products(request):
    products = CatalogProduct.objects.all().filter(active=True).order_by('-created')
    print(products)
    context = {
        "products": products,
    }

    if request.POST:
        if 'cart_id' in request.COOKIES:
            session = request.COOKIES['cart_id']
        else:
            session = get_random_string(100)
            Cart(session=session).save()
        count = request.POST.get('count')
        product = CatalogProduct.objects.get(id=request.POST.get('product'))
        cart = Cart.objects.get(session=session)
        item = Item(cart=cart, product=product, count=count)
        item.save()
        response = render(request, SITE_THEME + '/catalog/list_view.html', context)
        response.set_cookie('cart_id', session)
        return response

    return render(request, SITE_THEME + '/catalog/list_view.html', context)


def single_post(request, product_id):
    product = get_object_or_404(CatalogProduct, pk=product_id)
    context = {
        'product': product,
        'images': CatalogProduct.get_all_images(product_id),
    }
    return render(request, SITE_THEME + '/catalog/single-product.html', context)
