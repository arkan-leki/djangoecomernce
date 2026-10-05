"""Order emails: a confirmation to the customer and a heads-up to the store.

Nothing here is allowed to break checkout — the caller wraps every send in
try/except, so a mail outage leaves the order intact.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _send(subject, text_template, recipients, context, html_template=None):
    """Render and send one email. Returns True when it went out."""
    recipients = [r for r in recipients if r]
    if not recipients:
        logger.warning("No recipient for %r — nothing sent", subject)
        return False

    body = render_to_string(text_template, context)
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    if html_template:
        message.attach_alternative(render_to_string(html_template, context), "text/html")
    message.send(fail_silently=False)
    logger.info("Sent %r to %s", subject, ", ".join(recipients))
    return True


def send_order_emails(order, site_url=""):
    """Customer confirmation + store notification for a new order."""
    items = order.orderitem_set.select_related("product").all()
    context = {
        "order": order,
        "items": items,
        "site_url": site_url,
        "store_email": getattr(settings, "STORE_ORDER_EMAIL", ""),
    }
    sent = []

    # 1. the customer
    if order.email:
        try:
            _send(
                subject=f"Order #{order.id} confirmed — thank you!",
                text_template="payment/emails/order_confirmation.txt",
                recipients=[order.email],
                context=context,
                html_template="payment/emails/order_confirmation.html",
            )
            sent.append(f"customer:{order.email}")
        except Exception:  # noqa: BLE001 — never fail the order because of mail
            logger.exception("Order #%s: confirmation email to the customer failed", order.id)

    # 2. the shop owner
    store_email = getattr(settings, "STORE_ORDER_EMAIL", "")
    if store_email:
        try:
            _send(
                subject=f"New order #{order.id} — {order.amount_paid}",
                text_template="payment/emails/order_notification.txt",
                recipients=[store_email],
                context=context,
            )
            sent.append(f"store:{store_email}")
        except Exception:  # noqa: BLE001
            logger.exception("Order #%s: notification email to the store failed", order.id)

    return sent
