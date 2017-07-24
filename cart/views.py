from django.shortcuts import render
from .models import Item, Cart
from testsite.settings import SITE_THEME
from django.http import HttpResponseRedirect


def show_cart(request):
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
