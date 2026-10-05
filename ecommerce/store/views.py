from decimal import Decimal, InvalidOperation

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode

from store.models import Category, Product, Collection

# value -> (order_by field, label)
SORT_OPTIONS = {
    "newest": ("-id", "Newest"),
    "price_asc": ("price", "Price: low to high"),
    "price_desc": ("-price", "Price: high to low"),
    "name": ("title", "Name: A to Z"),
}


def shop(request):
    """Product listing with search, category/price filters, sort and a
    grid/list view toggle. Inspired by Suha's shop-grid.html / shop-list.html."""
    search_query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    view_mode = request.GET.get("view", "grid")
    if view_mode not in ("grid", "list"):
        view_mode = "grid"
    sort = request.GET.get("sort", "")
    if sort not in SORT_OPTIONS:
        sort = ""
    min_price = request.GET.get("min", "").strip()
    max_price = request.GET.get("max", "").strip()

    products = Product.objects.select_related("category").all()

    if search_query:
        products = products.filter(title__icontains=search_query)

    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            products = products.filter(category=active_category)
        else:
            category_slug = ""

    def _price(raw):
        try:
            return Decimal(raw)
        except (InvalidOperation, ValueError, TypeError):
            return None

    min_value, max_value = _price(min_price), _price(max_price)
    if min_value is None:
        min_price = ""
    else:
        products = products.filter(price__gte=min_value)
    if max_value is None:
        max_price = ""
    else:
        products = products.filter(price__lte=max_value)

    if sort:
        products = products.order_by(SORT_OPTIONS[sort][0])

    # Build URLs that preserve the other filters, so the view toggle, the sort
    # dropdown and the category chips all stay combinable.
    def qs(**overrides):
        params = {
            "q": search_query,
            "category": category_slug,
            "view": view_mode,
            "sort": sort,
            "min": min_price,
            "max": max_price,
        }
        params.update(overrides)
        clean = {
            k: v
            for k, v in params.items()
            if v and not (k == "view" and v == "grid")
        }
        base = reverse("shop")
        return f"{base}?{urlencode(clean)}" if clean else base

    context = {
        "products": products,
        "all_categories": Category.objects.all(),
        "search_query": search_query,
        "active_category": active_category,
        "category_slug": category_slug,
        "view_mode": view_mode,
        "sort": sort,
        "sort_options": SORT_OPTIONS,
        "min_price": min_price,
        "max_price": max_price,
        "grid_url": qs(view="grid"),
        "list_url": qs(view="list"),
        "clear_url": reverse("shop"),
        "has_filters": bool(
            search_query or category_slug or min_price or max_price or sort
        ),
        "category_urls": {
            c.slug: qs(category=c.slug, view=view_mode) for c in Category.objects.all()
        },
        "all_url": qs(category="", view=view_mode),
    }
    return render(request, "store/shop.html", context=context)


# Create your views here.
def store(request):
    # Supports the header search box: /?q=shoes
    search_query = request.GET.get("q", "").strip()
    all_products = Product.objects.all()
    if search_query:
        all_products = all_products.filter(title__icontains=search_query)
    collections = Collection.objects.all()
    context = {
        "all_products": all_products,
        "collections": collections,
        "search_query": search_query,
    }
    return render(request, "store/store.html", context=context)


def categories(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "store/list-category.html",
        context={"category": category, "products": products},
    )


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {"product": product}
    return render(request, "store/product-info.html", context=context)


def collection_detail(request, collection_slug):
    """One collection and its products.

    Collection.get_absolute_url() reverses 'collection-detail', which did not
    exist — using it in a template raised NoReverseMatch.
    """
    collection = get_object_or_404(Collection, slug=collection_slug)
    products = collection.products.select_related("category").all()
    context = {"collection": collection, "products": products}
    return render(request, "store/collection.html", context=context)
