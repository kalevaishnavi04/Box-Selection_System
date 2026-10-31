from django.urls import path

from . import views

urlpatterns = [
    path("recommend-box/", views.recommend_box, name="recommend-box"),
    path("orders/<int:order_id>/recommend-box/", views.recommend_for_order, name="recommend-order"),
    path("products/", views.products),
    path("products/add/", views.add_product),
    path("products/<int:product_id>/stock/", views.restock_product),
    path("products/<int:product_id>/image/", views.product_image_api, name="product-image-api"),
    path("orders/<int:order_id>/add-items/", views.add_items),
    path("boxes/", views.boxes),
    path("orders/", views.order_list),
    path("orders/place/", views.place_order),
    path("orders/<int:order_id>/accept/", views.accept_order),
    path("orders/<int:order_id>/pack/", views.pack_order),
    path("orders/<int:order_id>/cancel/", views.cancel_order),
    path("orders/<int:order_id>/items/<int:item_id>/unavailable/", views.mark_unavailable),
    path("requests/", views.request_list),
    path("requests/place/", views.place_request),
    path("requests/<int:request_id>/review/", views.review_request),
    path("orders/<int:order_id>/items/<int:item_id>/pick/", views.pick_item),
    path("history/", views.history, name="history"),
]

# Customer / warehouse workspace
urlpatterns += [
    path("auth/signup/", views.signup_api, name="signup-api"),
    path("auth/login/", views.login_api, name="login-api"),
    path("auth/logout/", views.logout_api, name="logout-api"),
    path("account/", views.account_api, name="account-api"),
    path("wishlist/", views.wishlist_api, name="wishlist-api"),
    path("wishlist/<int:product_id>/remove/", views.wishlist_remove_api, name="wishlist-remove-api"),
    path("support/", views.support_api, name="support-api"),
    path("my-requests/", views.my_requests_api, name="my-requests-api"),
    path("notifications/", views.notifications_api, name="notifications-api"),
    path("my-orders/", views.my_orders_api, name="my-orders-api"),
    path("my-orders/<int:order_id>/delete/", views.my_order_delete_api, name="my-order-delete-api"),
    path("warehouse/dashboard/", views.warehouse_dashboard_api, name="warehouse-dashboard-api"),
    path("warehouse/orders/<int:order_id>/delivery/", views.warehouse_delivery_update_api, name="warehouse-delivery-update-api"),
    path("warehouse/orders/<int:order_id>/location/", views.warehouse_location_update_api, name="warehouse-location-update-api"),
    path("warehouse/orders/<int:order_id>/send/", views.warehouse_send_order_api, name="warehouse-send-order-api"),
    path("warehouse/orders/<int:order_id>/delete/", views.warehouse_delete_order_api, name="warehouse-delete-order-api"),
    path("warehouse/orders/<int:order_id>/cancel/", views.warehouse_cancel_order_api, name="warehouse-cancel-order-api"),
    path("warehouse/orders/<int:order_id>/deliver/", views.warehouse_deliver_order_api, name="warehouse-deliver-order-api"),
    path("warehouse/profile/", views.account_api, name="warehouse-profile-api"),
    path("warehouse/tickets/<int:ticket_id>/reply/", views.warehouse_ticket_reply_api, name="warehouse-ticket-reply-api"),
]
