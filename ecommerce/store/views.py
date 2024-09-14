from django.shortcuts import get_object_or_404, render

from store.models import Category, Product, Collection


# Create your views here.
def store(request):
    all_products = Product.objects.all()
    collections = Collection.objects.all()
    context = {"all_products": all_products, "collections":collections}
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
