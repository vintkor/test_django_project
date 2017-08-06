from django.template.context_processors import request
from django.contrib import auth
from blog.models import Category
from cart.models import Item, Cart


def cart(request):
    if 'cart_id' in request.COOKIES:
        session = request.COOKIES.get('cart_id')
        cart = Cart.objects.get(session=session)
        items = Item.objects.filter(cart__session=session).count()
        return {
            'cart_count': items,
            # 'cart_total': cart.get_total_price
        }
    return {'cart_count': 0}


def categories(request):
    categories2 = Category.objects.all()
    context = {'nodes': categories2}
    return context


def user(request):
    user2 = auth.get_user(request)
    context = {'user': user2}
    return context
