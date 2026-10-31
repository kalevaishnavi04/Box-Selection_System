from django.core.management.base import BaseCommand

from packing.models import Box, Order, OrderItem, Product

BOXES = [
    ("Small", 20, 15, 10, 2, 10),
    ("Medium", 30, 20, 15, 5, 18),
    ("Large", 45, 35, 30, 15, 40),
]

# name, length, width, height, weight, fragile, stock
PRODUCTS = [
    ("Notebook", 21, 15, 2, 0.3, False, 40),
    ("Water bottle", 25, 7, 7, 0.5, False, 25),
    ("Coffee mug", 10, 10, 10, 0.4, True, 0),
    ("Desk lamp", 18, 18, 35, 1.2, False, 8),
    ("Backpack", 35, 25, 12, 0.9, False, 14),
    ("Wireless mouse", 12, 7, 4, 0.15, False, 30),
    ("Keyboard", 45, 15, 3, 0.8, False, 5),
    ("Headphones", 20, 18, 8, 0.35, False, 11),
    ("Phone stand", 12, 8, 8, 0.25, False, 3),
    ("Tiffin box", 20, 15, 8, 0.45, False, 19),
    ("Yoga mat", 60, 15, 15, 1.1, False, 9),
    ("Table fan", 35, 25, 20, 2.4, False, 4),
]


class Command(BaseCommand):
    help = "Load the QuickPack shop demo catalogue and sample boxes."

    def handle(self, *args, **opts):
        for n, l, w, h, mw, c in BOXES:
            Box.objects.update_or_create(
                name=n,
                defaults=dict(length=l, width=w, height=h, max_weight=mw, cost=c),
            )

        # Remove products from the older demo catalogue (keep any other custom products).
        Product.objects.filter(name__in=[
            "Bluetooth earphones", "Dumbbell", "Glass vase", "Phone case",
            "Pen", "Pencil box", "Chocolate bar", "Study table",
        ]).delete()

        for n, l, w, h, kg, fragile, stock in PRODUCTS:
            defaults = dict(
                length=l, width=w, height=h, weight=kg,
                fragile=fragile, stock=stock,
            )
            Product.objects.update_or_create(name=n, defaults=defaults)

        if not Order.objects.exists():
            order = Order.objects.create(customer_name="Ravi")
            for name in ("Notebook", "Water bottle"):
                OrderItem.objects.get_or_create(
                    order=order, product=Product.objects.get(name=name)
                )

        self.stdout.write(self.style.SUCCESS(
            "QuickPack demo catalogue loaded: 12 shop products."
        ))
