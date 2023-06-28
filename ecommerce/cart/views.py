from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from store.models import Product


# Create your views here.
def cart_summary(request):
    cart = Cart(request)

    return render(request, "cart/cart-summary.html", {'cart': cart})


@csrf_exempt  # Only for demonstration purposes, should be used with caution
@require_POST
def cart_add(request):
    cart = Cart(request)
    # Get the product_id and product_quantity from the POST data
    product_id = int(request.POST.get("product_id"))
    product_quantity = int(request.POST.get("product_quantity"))

    # Perform necessary operations with the product_id and product_quantity
    # For example, add the product to the user's shopping cart
    product = get_object_or_404(Product, pk=product_id)
    cart.add(product=product, product_qyt=product_quantity)

    cart_quantity = cart.__len__()

    # Return a JSON response indicating the success of the operation
    response_data = {
        "success": True,
        "product_title": product.title,
        "cart_quantity": cart_quantity,
    }
    return JsonResponse(response_data)

@csrf_exempt  # Only for demonstration purposes, should be used with caution
@require_POST
def cart_update(request):
    cart = Cart(request)
    # Get the product_id and product_quantity from the POST data
    product_id = str(request.POST.get("product_id"))
    product_quantity = int(request.POST.get("product_quantity"))

    # Perform necessary operations with the product_id and product_quantity
    # For example, add the product to the user's shopping cart
    cart.update(product_id=product_id, product_qyt=product_quantity)

    cart_quantity = cart.__len__()
    cart_total = cart.get_total()

    # Return a JSON response indicating the success of the operation
    response_data = {
        "success": True,
        "cart_total": cart_total,
        "cart_quantity": cart_quantity,
    }
    return JsonResponse(response_data)


@csrf_exempt  # Only for demonstration purposes, should be used with caution
@require_POST
def cart_delete(request):
    cart = Cart(request)
    # Get the product_id and product_quantity from the POST data
    product_id = str(request.POST.get("product_id"))
    # Perform necessary operations with the product_id 
    # For example, delete the product to the user's shopping cart

    cart.delete(product_id=product_id)
        

    cart_quantity = cart.__len__()
    cart_total = cart.get_total()

    # Return a JSON response indicating the success of the operation
    response_data = {
        "success": True,
        "cart_quantity": cart_quantity,
        "cart_total": cart_total
    }
    return JsonResponse(response_data)
