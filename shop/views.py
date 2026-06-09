from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .models import Category, Product


def home(request):
    featured_products = Product.objects.filter(is_available=True)[:3]
    return render(
        request,
        "shop/home.html",
        {"featured_products": featured_products},
    )


def catalog(request):
    products = Product.objects.filter(is_available=True).select_related("category")
    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    search_query = request.GET.get("q", "").strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get("sort", "newest")
    sort_options = {
        "newest": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
        "name": "name",
    }
    products = products.order_by(sort_options.get(sort, "-created_at"))

    return render(
        request,
        "shop/catalog.html",
        {
            "products": products,
            "categories": categories,
            "current_category": category_slug,
            "search_query": search_query,
            "min_price": min_price or "",
            "max_price": max_price or "",
            "current_sort": sort,
        },
    )


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart.add(product)
    messages.success(request, f"«{product.name}» добавлен в корзину.")
    next_url = request.POST.get("next", "shop:catalog")
    return redirect(next_url)


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"«{product.name}» удалён из корзины.")
    return redirect("shop:cart")


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    cart.update(product, quantity)
    return redirect("shop:cart")


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Корзина очищена.")
    return redirect("shop:cart")
