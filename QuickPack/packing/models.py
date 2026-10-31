from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

from .services import BoxSpec, Item

POSITIVE = [MinValueValidator(0.01)]


class Product(models.Model):
    """Dimensions in cm, weight in kg."""
    name = models.CharField(max_length=120)
    length = models.FloatField(validators=POSITIVE)
    width = models.FloatField(validators=POSITIVE)
    height = models.FloatField(validators=POSITIVE)
    weight = models.FloatField(validators=POSITIVE)
    fragile = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)   # units available in the warehouse
    image = models.ImageField(upload_to="products/", null=True, blank=True)   # optional product photo

    def __str__(self):
        return self.name

    def to_item(self):
        return Item(self.name, self.length, self.width, self.height, self.weight, self.fragile)


class Box(models.Model):
    """INTERNAL dimensions in cm, max weight in kg, cost in rupees."""
    name = models.CharField(max_length=60, unique=True)
    length = models.FloatField(validators=POSITIVE)
    width = models.FloatField(validators=POSITIVE)
    height = models.FloatField(validators=POSITIVE)
    max_weight = models.FloatField(validators=POSITIVE)
    cost = models.FloatField(validators=POSITIVE)

    class Meta:
        verbose_name_plural = "boxes"

    def __str__(self):
        return f"{self.name} (Rs {self.cost:g})"

    def to_spec(self):
        return BoxSpec(self.name, self.length, self.width, self.height,
                       self.max_weight, self.cost, self.id)


class Order(models.Model):
    PLACED, ACCEPTED, PACKED, CANCELLED = "placed", "accepted", "packed", "cancelled"
    OUT, DELIVERED = "out_for_delivery", "delivered"
    STATUSES = [(PLACED, "Placed"), (ACCEPTED, "Accepted"), (PACKED, "Packed"),
                (OUT, "Out for delivery"), (DELIVERED, "Delivered"), (CANCELLED, "Cancelled")]
    customer_name = models.CharField(max_length=80, default="Guest")
    customer = models.ForeignKey(User, null=True, blank=True, related_name="packing_orders", on_delete=models.SET_NULL)
    delivery_address = models.TextField(blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)
    delivery_person = models.CharField(max_length=80, blank=True)
    delivery_person_phone = models.CharField(max_length=20, blank=True)
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_location_updated_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, default="pending", choices=[("pending", "Pending"), ("paid_demo", "Paid (demo)"), ("failed", "Failed"), ("cod", "Cash on delivery")])
    status = models.CharField(max_length=20, choices=STATUSES, default=PLACED)
    packed_boxes = models.JSONField(default=list, blank=True)   # [{"box": "Medium", "cost": 18}]
    hidden_for_customer = models.BooleanField(default=False)    # "deleted" from the customer's list (row is kept)
    hidden_for_warehouse = models.BooleanField(default=False)   # "deleted" from the warehouse list (row is kept)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unavailable = models.BooleanField(default=False)   # warehouse could not supply it
    picked = models.PositiveIntegerField(default=0)     # how many the packer has picked from the shelf


class Recommendation(models.Model):
    """Audit trail: every request and the answer we gave."""
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    request_payload = models.JSONField()
    result = models.JSONField()
    status = models.CharField(max_length=20)
    total_cost = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]


class ProductRequest(models.Model):
    """A customer asks for an item that is not in the catalogue.
    It does NOT become a Product until a warehouse employee approves it."""
    PENDING, AVAILABLE = "pending", "available"
    TEMPORARY, NOT_AVAILABLE = "temporarily_unavailable", "not_available"
    STATUSES = [(PENDING, "Under review"), (AVAILABLE, "Available"),
                (TEMPORARY, "Temporarily unavailable"), (NOT_AVAILABLE, "Not available / not supported")]
    customer_name = models.CharField(max_length=80)
    user = models.ForeignKey(User, null=True, blank=True, related_name="item_requests", on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=30, choices=STATUSES, default=PENDING)
    restock_days = models.PositiveSmallIntegerField(null=True, blank=True)   # 1 or 2
    reason = models.CharField(max_length=200, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"


class CustomerProfile(models.Model):
    CUSTOMER, WAREHOUSE = "customer", "warehouse"
    ROLES = [(CUSTOMER, "Customer"), (WAREHOUSE, "Warehouse staff")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    role = models.CharField(max_length=20, choices=ROLES, default=CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notifications_enabled = models.BooleanField(default=True)
    payment_preference = models.CharField(max_length=20, default="cod", choices=[("cod", "Cash on delivery"), ("upi", "UPI (demo preference)"), ("card", "Card (demo preference)")])

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [("user", "product")]


class SupportTicket(models.Model):
    OPEN, IN_PROGRESS, RESOLVED = "open", "in_progress", "resolved"
    STATUSES = [(OPEN, "Open"), (IN_PROGRESS, "In progress"), (RESOLVED, "Resolved")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_tickets")
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=120)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUSES, default=OPEN)
    staff_reply = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quickpack_notifications")
    title = models.CharField(max_length=120)
    message = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
