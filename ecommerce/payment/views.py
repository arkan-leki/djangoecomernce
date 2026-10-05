import logging

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from cart.cart import Cart
from payment.emails import send_order_emails
from payment.models import Order

from payment.models import ShippingAddress

logger = logging.getLogger(__name__)


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


@transaction.atomic
def complete_order(request):
    if request.POST.get("action") == "complete_order":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "").strip()
        address1 = request.POST.get("address1", "")
        address2 = request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zipcode = request.POST.get("zipcode", "")

        ShippingAddress = (
            address1 + " \n" + address2 + " \n" + city + " \n" + state + " \n" + zipcode
        )

        cart = Cart(request)
        # Cart.__iter__ prunes items whose product no longer exists, so build the
        # item list first: everything below is derived from what really is in the
        # basket, and an empty basket never produces a $0 order.
        cart_items = list(cart)
        if not cart_items:
            return JsonResponse(
                {"success": False, "error": "Your basket is empty."}, status=400
            )
        total_cost = sum(item["total"] for item in cart_items)

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                full_name=name,
                email=email,
                phone=phone or None,
                shipping_address=ShippingAddress,
                amount_paid=total_cost,
            )
            for item in cart_items:
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
                phone=phone or None,
                shipping_address=ShippingAddress,
                amount_paid=total_cost,
            )
            for item in cart_items:
                order.orderitem_set.create(
                    product=item["product"],
                    quantity=item["qyt"],
                    price=item["price"],
                )
        order_success = True

        # Confirmation to the customer + notification to the store. Wrapped in
        # try/except inside send_order_emails so a mail failure can never undo
        # an order that has already been written.
        try:
            sent_to = send_order_emails(order, site_url=request.build_absolute_uri("/"))
            logger.info("Order #%s emails: %s", order.id, sent_to or "none")
        except Exception:  # noqa: BLE001
            logger.exception("Order #%s: unexpected failure sending emails", order.id)

        return JsonResponse({"success": order_success, "order_id": order.id})
    return JsonResponse(
        {"success": False, "error": "This endpoint expects action=complete_order."},
        status=400,
    )
