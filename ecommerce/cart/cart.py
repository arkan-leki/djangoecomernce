from decimal import Decimal
import decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("cart_session")

        if "cart_session" not in request.session:
            cart = self.session["cart_session"] = {}

        self.cart = cart

    def add(self, product, product_qyt):
        product_id = product.id

        if product_id in self.cart:
            self.cart[product_id]["qyt"] = product_qyt
        else:
            self.cart[product_id] = {"price": str(product.price), "qyt": product_qyt}

        self.session.modified = True

    def delete(self, product_id):
        
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product_id, product_qyt):

        if product_id in self.cart:
            self.cart[product_id]["qyt"] = product_qyt

        self.session.modified = True

    def __len__(self):
        return sum(item["qyt"] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = Decimal(item["price"] * item["qyt"])
            yield item

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
    # clean 
    def clear(self):
        del self.session["cart_session"]
        self.session.modified = True
