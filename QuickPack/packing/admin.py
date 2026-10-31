from django.contrib import admin

from .models import (Box, Order, OrderItem, Product, ProductRequest, Recommendation,
                     CustomerProfile, WishlistItem, SupportTicket, UserNotification)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "length", "width", "height", "weight", "fragile", "image")
    search_fields = ("name",)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ("name", "length", "width", "height", "max_weight", "cost")


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "total_cost", "created_at")
    readonly_fields = ("request_payload", "result", "status", "total_cost", "order")


@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "customer_name", "quantity", "status", "restock_days")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "notifications_enabled")
    list_filter = ("role", "notifications_enabled")
    search_fields = ("user__username", "user__email", "phone")

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "subject", "message")

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    list_filter = ("is_read",)
