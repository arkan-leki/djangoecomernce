from decimal import Decimal
import decimal
from store.models import Product
import uuid
import json


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("cart_session")

        if "cart_session" not in request.session:
            cart = self.session["cart_session"] = {}

        self.cart = cart

    def _generate_cart_item_id(self):
        """Generate a unique ID for a new cart item."""
        return str(uuid.uuid4())

    def add(self, product, product_qyt, size, color):
        product_id = product.id

        # Check if product with the same size and color already exists in the cart
        for item_id, item in self.cart.items():
            if (item['product_id'] == product_id and
                item['size'] == size and
                item['color'] == color):
                # Update quantity if found
                self.cart[item_id]["qyt"] += product_qyt
                self.session.modified = True
                return
        
        # If not found, create a new entry with a unique cart item ID
        cart_item_id = self._generate_cart_item_id()
        self.cart[cart_item_id] = {
            "product_id": product_id,
            "price": str(product.price),
            "qyt": product_qyt,
            "size": size,
            "color": color
        }

        self.session.modified = True

    def delete(self, cart_item_id):
        if cart_item_id in self.cart:
            del self.cart[cart_item_id]
        self.session.modified = True

    def update(self, cart_item_id, product_qyt):
        if cart_item_id in self.cart:
            self.cart[cart_item_id]["qyt"] = product_qyt
        self.session.modified = True

    def __len__(self):
        return sum(item["qyt"] for item in self.cart.values())

    def _prune_stale(self):
        """Drop entries whose product no longer exists.

        A product can be deleted — or the whole catalogue re-seeded — while it
        is still sitting in someone's session cart. Those entries used to be
        yielded by __iter__ without a "product" key, so checkout crashed with
        KeyError('product') and the shopper saw the payment-failed page.
        """
        stale = [
            key
            for key, item in self.cart.items()
            if not Product.objects.filter(id=item["product_id"]).exists()
        ]
        for key in stale:
            self.cart.pop(key, None)
        if stale:
            self.session.modified = True
        return len(stale)

    def __iter__(self):
        self._prune_stale()
        product_ids = [item["product_id"] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        # DEEP copy: self.cart IS the session payload, and this iterator writes
        # Decimal prices/totals into each entry. With a shallow copy those
        # Decimals landed in the session and blew up on save with
        # "TypeError: Object of type Decimal is not JSON serializable".
        cart = {key: dict(item) for key, item in self.cart.items()}

        for product in products:
            for item_id, item in cart.items():
                if item["product_id"] == product.id:
                    item["product"] = product

        for item in cart.values():
            if "product" not in item:
                # belt and braces: never yield an item we cannot resolve
                continue
            item["price"] = Decimal(item["price"])
            item["total"] = Decimal(item["price"]) * Decimal(item["qyt"])
            yield item  # Ensure this yields dictionaries, not tuples

    def to_json(self):
        items = []
        stale_keys = []
        for key, item in self.cart.items():
            product_id = item['product_id']
            # A product can be deleted (or the catalogue re-seeded) while it is
            # still sitting in someone's session cart. Product.objects.get()
            # raised DoesNotExist here and turned /cart/fetch/ into a 500.
            product = Product.objects.filter(id=product_id).first()
            if product is None:
                stale_keys.append(key)
                continue
            total = Decimal(item["price"]) * Decimal(item["qyt"])
            items.append({
                'id': key,
                'product': {
                    'title': product.title if hasattr(product, 'title') else '',
                    'image': product.image.url if hasattr(product, 'image') and product.image else '',
                    'url': product.get_absolute_url() if hasattr(product, 'get_absolute_url') else ''
                },
                'price': str(item['price']),
                'qyt': item['qyt'],
                'size': item['size'],
                'color': item['color'],
                'total': str(total)
            })

        # prune dead references so the cart heals itself
        for key in stale_keys:
            self.cart.pop(key, None)
        if stale_keys:
            self.session.modified = True

        return json.dumps({
            'cart_items': items,
            'cart_total': str(self.get_total())
        })


    def get_total(self):
        # stale entries must not be billed: the total has to match the items
        # that complete_order() can actually turn into OrderItems
        self._prune_stale()
        try:
            return sum(
                Decimal(item["price"]) * Decimal(item["qyt"])
                for item in self.cart.values()
            )
        except decimal.ConversionSyntax as e:
            for item in self.cart.values():
                print("ConversionSyntax exception occurred:")
                print("Price:", item["price"])
                print("Quantity:", item["qyt"])
            raise e

    def clear(self):
        del self.session["cart_session"]
        self.session.modified = True
