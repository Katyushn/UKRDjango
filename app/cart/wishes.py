from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Wishes(object):

    def __init__(self, request):
        self.session = request.session
        wishes = self.session.get(settings.WISHES_SESSION_ID)
        if not wishes:
            wishes = self.session[settings.WISHES_SESSION_ID] = {}
        self.wishes = wishes

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.wishes:
            self.wishes[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.wishes[product_id]['quantity'] = 1
        else:
            self.wishes[product_id]['quantity'] = 1
        self.save()

    def save(self):
        self.session[settings.WISHES_SESSION_ID] = self.wishes
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.wishes:
            del self.wishes[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.wishes.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.wishes[str(product.id)]['product'] = product

        for item in self.wishes.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.wishes.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.wishes.values())

    def clear(self):
        del self.session[settings.WISHES_SESSION_ID]
        self.session.modified = True
