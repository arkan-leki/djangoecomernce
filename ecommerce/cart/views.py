from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

from cart.cart import Cart
from store.models import Product
import json


# Cart summary view
def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart/cart-summary.html", {'cart': cart})


def cart_data(request):
    cart = Cart(request)
    return JsonResponse(json.loads(cart.to_json()), safe=False)


@require_POST
def cart_add(request):
    cart = Cart(request)
    
    # Get product data from POST request
    try:
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))
        size = request.POST.get("size")
        color = request.POST.get("color")
    except (ValueError, TypeError) as e:
        return JsonResponse({"success": False, "error": "Invalid input data"}, status=400)
    
    # Fetch the product
    product = get_object_or_404(Product, pk=product_id)

    # Add the product to the cart
    cart.add(product=product, product_qyt=product_quantity, size=size, color=color)

    # Get cart summary data
    cart_quantity = cart.__len__()

    # Return success response
    response_data = {
        "success": True,
        "product_title": product.title,
        "cart_quantity": cart_quantity,
        "csrf_token": get_token(request)  # Return CSRF token for AJAX requests
    }
    return JsonResponse(response_data)

@require_POST
def cart_update(request):
    cart = Cart(request)
    
    # Read and parse JSON data from request body
    try:
        data = json.loads(request.body)
        cart_item_id = str(data.get("cart_item_id"))
        product_quantity = int(data.get("product_quantity"))  # Convert to int if necessary
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        return JsonResponse({"success": False, "error": f"Invalid input data or {e}"}, status=400)

    # Check if cart_item_id and product_quantity are valid
    if not cart_item_id or product_quantity is None:
        return JsonResponse({"success": False, "error": "Missing cart item ID or quantity"}, status=400)

    # Update the quantity of the cart item
    cart.update(cart_item_id=cart_item_id, product_qyt=product_quantity)

    # Get cart summary data
    cart_quantity = len(cart)  # Use len(cart) to get the number of items
    cart_total = cart.get_total()

    # Return success response
    response_data = {
        "success": True,
        "cart_total": cart_total,
        "cart_quantity": cart_quantity,
        "csrf_token": get_token(request)  # Return CSRF token for AJAX requests
    }
    return JsonResponse(response_data)

@require_POST
def cart_delete(request):
    cart = Cart(request)
    
    # Read and parse JSON data from request body
    try:
        data = json.loads(request.body)
        cart_item_id = str(data.get("cart_item_id"))
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid input data"}, status=400)

    # Validate if cart_item_id was retrieved correctly
    if not cart_item_id:
        return JsonResponse({"success": False, "error": "No cart item ID provided"}, status=400)

    # Delete the cart item
    print(cart_item_id)
    cart.delete(cart_item_id)

    # Get cart summary data
    cart_quantity = cart.__len__()
    cart_total = cart.get_total()

    # Return success response
    response_data = {
        "success": True,
        "cart_quantity": cart_quantity,
        "cart_total": cart_total,
        "csrf_token": get_token(request)  # Return CSRF token for AJAX requests
    }
    return JsonResponse(response_data)
