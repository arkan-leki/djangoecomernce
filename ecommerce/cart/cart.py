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
        print(cart_item_id)
        if cart_item_id in self.cart:
            print(self.cart[cart_item_id])
            del self.cart[cart_item_id]
        self.session.modified = True

    def update(self, cart_item_id, product_qyt):
        if cart_item_id in self.cart:
            self.cart[cart_item_id]["qyt"] = product_qyt
        self.session.modified = True

    def __len__(self):
        return sum(item["qyt"] for item in self.cart.values())

    def __iter__(self):
        product_ids = [item["product_id"] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            for item_id, item in cart.items():
                if item["product_id"] == product.id:
                    item["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = Decimal(item["price"]) * Decimal(item["qyt"])
            yield item  # Ensure this yields dictionaries, not tuples

    def to_json(self):
        items = []
        for  key, item in self.cart.items():
            product_id = item['product_id']
            product = Product.objects.get(id=product_id)
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

        return json.dumps({
            'cart_items': items,
            'cart_total': str(self.get_total())
        })


    def get_total(self):
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
