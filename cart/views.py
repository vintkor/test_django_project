from django.shortcuts import render
from .models import Item, Cart
from testsite.settings import SITE_THEME
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST


def show_cart(request):
    items = []
    cart = ''
    if 'cart_id' in request.COOKIES:
        session = request.COOKIES.get('cart_id')
        items = Item.objects.filter(cart__session=session)
        cart = Cart.objects.get(session=session)
    context = {'items': items, 'cart': cart}
    return render(request, SITE_THEME + '/cart/cart.html', context)


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_POST
def update_cart(request):
    product = Item.objects.get(id=request.POST.get('product_id'))
    cart = Cart.objects.get(session=request.COOKIES.get('cart_id'))
    Item.update_count(product=product, cart=cart, count=request.POST.get('count'), update=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))