from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from cart.cart import Cart
from payment.models import Order

from payment.models import ShippingAddress


# Create your views here.
def payment_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "payment/success.html")


def payment_failed(request):
    return render(request, "payment/failed.html")


def checkout(request):
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
            context = {"shipping_address": shipping_address}
            return render(request, "payment/checkout.html", context)

        except:  # noqa: E722
            return render(request, "payment/checkout.html")

    return render(request, "payment/checkout.html")


def complete_order(request):
    if request.POST.get("action") == "complete_order":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        address1 = request.POST.get("address1", "")
        address2 = request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zipcode = request.POST.get("zipcode", "")

        ShippingAddress = (
            address1 + " \n" + address2 + " \n" + city + " \n" + state + " \n" + zipcode
        )

        cart = Cart(request)
        total_cost = cart.get_total()

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                full_name=name,
                email=email,
                shipping_address=ShippingAddress,
                amount_paid=total_cost,
            )
            for item in cart:
                order.orderitem_set.create(
                    product=item["product"],
                    quantity=item["qyt"],
                    price=item["price"],
                    user=request.user,
                )
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=ShippingAddress,
                amount_paid=total_cost,
            )
            for item in cart:
                order.orderitem_set.create(
                    product=item["product"],
                    quantity=item["qyt"],
                    price=item["price"],
                )
        order_success = True
        response = JsonResponse({"success": order_success})
        return HttpResponse(response)
    return HttpResponse("App_Name:Name")
