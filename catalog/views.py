from django.shortcuts import render, get_object_or_404
from catalog.models import CatalogProduct, CatalogCategory
from testsite.settings import SITE_THEME
from cart.models import Cart, Item
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def add_to_cart(request, context, view):
    if request.POST:
        if 'cart_id' in request.COOKIES:
            session = request.COOKIES['cart_id']
        else:
            session = get_random_string(100)
            Cart(session=session).save()
        Item.add_to_cart(product_id=request.POST.get('product'), session=session, count=request.POST.get('count'))
        response = render(request, SITE_THEME + view, context)
        response.set_cookie('cart_id', session, max_age=365*24*60*60)
        return response


def all_products(request):
    root_categories = CatalogCategory.objects.filter(level=0)
    products_list = CatalogProduct.objects.all().filter(active=True).order_by('-created')
    paginator = Paginator(products_list, 20)

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    list_pages = []
    for page in range(0, paginator.num_pages):
        list_pages.append(page+1)

    context = {"products": products, "list_pages": list_pages, 'root_categories': root_categories}
    if request.POST:
        response = add_to_cart(request=request, context=context, view='/catalog/list_view.html')
        return response

    return render(request, SITE_THEME + '/catalog/list_view.html', context)


def cat_products(request, cat_id):
    category = CatalogCategory.objects.get(id=cat_id)
    descendants = category.get_descendants(include_self=True)
    products_list = CatalogProduct.objects.filter(active=True, category__in=descendants).order_by('-created')
    paginator = Paginator(products_list, 20)

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    list_pages = []
    for page in range(0, paginator.num_pages):
        list_pages.append(page + 1)

    context = {"products": products, "list_pages": list_pages, 'category': category}
    if request.POST:
        response = add_to_cart(request=request, context=context, view='/catalog/list_view.html')
        return response

    return render(request, SITE_THEME + '/catalog/list_view.html', context)


def single_post(request, product_id):
    product = get_object_or_404(CatalogProduct, pk=product_id)
    context = {
        'product': product,
        'images': CatalogProduct.get_all_images(product_id),
    }
    if request.POST:
        response = add_to_cart(request=request, context=context, view='/catalog/single-product.html')
        return response
    return render(request, SITE_THEME + '/catalog/single-product.html', context)



