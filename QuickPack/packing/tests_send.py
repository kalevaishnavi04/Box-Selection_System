import json

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Box, CustomerProfile, Order, OrderItem, Product


class SendOrderTests(TestCase):
    """Warehouse last steps: packed -> out for delivery -> delivered."""

    def setUp(self):
        Box.objects.create(name="Medium", length=30, width=20, height=15, max_weight=5, cost=18)
        self.p = Product.objects.create(name="Notebook", length=21, width=15, height=2, weight=0.3, stock=9)
        self.cust = User.objects.create_user("asha", password="Asha-pass-123")
        CustomerProfile.objects.get_or_create(user=self.cust)
        staff = User.objects.create_user("wh", password="Wh-pass-123")
        prof, _ = CustomerProfile.objects.get_or_create(user=staff)
        prof.role = "warehouse"
        prof.save()
        self.order = Order.objects.create(customer_name="Asha", customer=self.cust, status="packed")
        OrderItem.objects.create(order=self.order, product=self.p, quantity=1, picked=1)

    def send(self, data):
        return self.client.post(f"/api/warehouse/orders/{self.order.id}/send/", json.dumps(data),
                                content_type="application/json")

    def test_needs_warehouse_login(self):
        self.assertIn(self.send({}).status_code, (302, 401))
        self.client.login(username="asha", password="Asha-pass-123")
        self.assertEqual(self.send({"delivery_person": "R", "delivery_person_phone": "9000000002"}).status_code, 403)

    def test_send_then_deliver_notifies_customer(self):
        self.client.login(username="wh", password="Wh-pass-123")
        self.assertEqual(self.send({"delivery_person": "", "delivery_person_phone": "123"}).status_code, 400)
        self.assertEqual(self.send({"delivery_person": "Ramesh", "delivery_person_phone": "9000000002",
                                    "eta_minutes": 1}).status_code, 400)
        r = self.send({"delivery_person": "Ramesh", "delivery_person_phone": "9000000002", "eta_minutes": 25})
        self.assertEqual(r.status_code, 200, r.content)
        self.order.refresh_from_db()
        self.assertEqual((self.order.status, self.order.delivery_person), ("out_for_delivery", "Ramesh"))
        self.assertIsNotNone(self.order.estimated_delivery)
        self.assertEqual(self.send({"delivery_person": "Ramesh", "delivery_person_phone": "9000000002"}).status_code, 409)
        self.assertEqual(self.client.post(f"/api/warehouse/orders/{self.order.id}/deliver/").status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "delivered")
        self.assertEqual(self.client.post(f"/api/warehouse/orders/{self.order.id}/deliver/").status_code, 409)
        self.assertEqual(self.cust.quickpack_notifications.count(), 2)

    def test_cannot_send_an_order_that_is_not_packed(self):
        self.client.login(username="wh", password="Wh-pass-123")
        Order.objects.filter(pk=self.order.id).update(status="accepted")
        self.assertEqual(self.send({"delivery_person": "Ramesh", "delivery_person_phone": "9000000002"}).status_code, 409)


from django.test import override_settings


@override_settings(DEBUG=True, ALLOWED_HOSTS=["127.0.0.1", "shop.example.com"], QUICKPACK_DEMO_AUTOLOGIN=True)
class WorkspaceRoleLoginTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        from packing.models import CustomerProfile
        self.customer = User.objects.create_user(username="customer-login", password="Customer-pass-123")
        CustomerProfile.objects.create(user=self.customer, role=CustomerProfile.CUSTOMER)
        self.warehouse = User.objects.create_user(username="warehouse-login", password="Warehouse-pass-123")
        CustomerProfile.objects.create(user=self.warehouse, role=CustomerProfile.WAREHOUSE)

    def test_customer_cannot_open_warehouse_workspace(self):
        r = self.client.post("/api/auth/login/", data='{"username":"customer-login","password":"Customer-pass-123"}', content_type="application/json", HTTP_X_WORKSPACE="warehouse")
        self.assertEqual(r.status_code, 403)

    def test_warehouse_cannot_open_customer_workspace(self):
        r = self.client.post("/api/auth/login/", data='{"username":"warehouse-login","password":"Warehouse-pass-123"}', content_type="application/json", HTTP_X_WORKSPACE="customer")
        self.assertEqual(r.status_code, 403)

    def test_customer_login_works_in_customer_workspace(self):
        r = self.client.post("/api/auth/login/", data='{"username":"customer-login","password":"Customer-pass-123"}', content_type="application/json", HTTP_X_WORKSPACE="customer")
        self.assertEqual(r.status_code, 200)

    def test_warehouse_login_works_in_warehouse_workspace(self):
        r = self.client.post("/api/auth/login/", data='{"username":"warehouse-login","password":"Warehouse-pass-123"}', content_type="application/json", HTTP_X_WORKSPACE="warehouse")
        self.assertEqual(r.status_code, 200)


class TicketReplyAndItemRequestTests(TestCase):
    """Customer message -> warehouse reply comes back; customer item request -> warehouse answer comes back."""

    def setUp(self):
        self.cust = User.objects.create_user("asha", password="Asha-pass-123", first_name="Asha")
        CustomerProfile.objects.get_or_create(user=self.cust)
        staff = User.objects.create_user("wh", password="Wh-pass-123")
        prof, _ = CustomerProfile.objects.get_or_create(user=staff)
        prof.role = "warehouse"
        prof.save()
        self.cust_client, self.wh_client = self.client_class(), self.client_class()
        self.cust_client.login(username="asha", password="Asha-pass-123")
        self.wh_client.login(username="wh", password="Wh-pass-123")

    def post(self, c, url, data):
        return c.post(url, json.dumps(data), content_type="application/json")

    def test_warehouse_reply_reaches_customer(self):
        t = self.post(self.cust_client, "/api/support/", {"subject": "Bad order", "message": "Order is not good"}).json()
        # empty reply is refused
        self.assertEqual(self.post(self.wh_client, f"/api/warehouse/tickets/{t['id']}/reply/", {"reply": "  "}).status_code, 400)
        r = self.post(self.wh_client, f"/api/warehouse/tickets/{t['id']}/reply/",
                      {"reply": "Sorry about this, we will replace it.", "status": "resolved"})
        self.assertEqual(r.status_code, 200)
        mine = self.cust_client.get("/api/support/").json()["tickets"][0]
        self.assertEqual((mine["reply"], mine["status"]), ("Sorry about this, we will replace it.", "resolved"))
        note = self.cust.quickpack_notifications.get()
        self.assertIn("Sorry about this", note.message)

    def test_item_request_answers_reach_customer(self):
        r = self.post(self.cust_client, "/api/requests/place/", {"name": "Table", "quantity": 1})
        self.assertEqual(r.status_code, 201)
        rid = r.json()["id"]
        self.assertEqual(self.cust_client.get("/api/my-requests/").json()["requests"][0]["status"], "pending")
        self.assertEqual(len(self.wh_client.get("/api/warehouse/dashboard/").json()["item_requests"]), 1)
        # not in stock now: back in 2 days
        r = self.post(self.wh_client, f"/api/requests/{rid}/review/", {"decision": "temporarily_unavailable", "restock_days": 2})
        self.assertEqual(r.status_code, 200)
        mine = self.cust_client.get("/api/my-requests/").json()["requests"][0]
        self.assertIn("2 days", mine["reply"])
        self.assertIn("2 days", self.cust.quickpack_notifications.latest("id").message)
        # later approved -> product created and customer told
        r = self.post(self.wh_client, f"/api/requests/{rid}/review/",
                      {"decision": "available", "length": 120, "width": 60, "height": 75, "weight": 15, "stock": 3})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Product.objects.filter(name="Table").exists())
        self.assertIn("available", self.cust.quickpack_notifications.latest("id").message)
        self.assertEqual(self.cust.quickpack_notifications.count(), 2)


class CancelOrderBothSidesTests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name="Notebook", length=21, width=15, height=2, weight=0.3, stock=5)
        self.cust = User.objects.create_user("asha", password="Asha-pass-123")
        CustomerProfile.objects.get_or_create(user=self.cust)
        self.other = User.objects.create_user("ravi", password="Ravi-pass-123")
        staff = User.objects.create_user("wh", password="Wh-pass-123")
        prof, _ = CustomerProfile.objects.get_or_create(user=staff)
        prof.role = "warehouse"
        prof.save()
        self.c, self.w, self.o = self.client_class(), self.client_class(), self.client_class()
        self.c.login(username="asha", password="Asha-pass-123")
        self.w.login(username="wh", password="Wh-pass-123")
        self.o.login(username="ravi", password="Ravi-pass-123")

    def make(self, status):
        order = Order.objects.create(customer_name="Asha", customer=self.cust, status=status)
        OrderItem.objects.create(order=order, product=self.p, quantity=2)
        return order

    def test_customer_cancels_own_placed_order_and_stock_returns(self):
        order = self.make("placed")
        mine = self.c.get("/api/my-orders/").json()["orders"][0]
        self.assertTrue(mine["can_cancel"])
        self.assertEqual(mine["items"][0]["name"], "Notebook")
        self.assertEqual(self.o.post(f"/api/orders/{order.id}/cancel/").status_code, 403)
        self.assertEqual(self.c.post(f"/api/orders/{order.id}/cancel/").status_code, 200)
        self.p.refresh_from_db(); order.refresh_from_db()
        self.assertEqual((order.status, self.p.stock), ("cancelled", 7))

    def test_customer_cannot_cancel_after_accept(self):
        order = self.make("accepted")
        self.assertFalse(self.c.get("/api/my-orders/").json()["orders"][0]["can_cancel"])
        self.assertEqual(self.c.post(f"/api/orders/{order.id}/cancel/").status_code, 409)

    def test_warehouse_cancels_accepted_or_packed_order_and_customer_is_told(self):
        for status in ("accepted", "packed"):
            order = self.make(status)
            r = self.w.post(f"/api/warehouse/orders/{order.id}/cancel/", json.dumps({"reason": "Damaged stock"}),
                            content_type="application/json")
            self.assertEqual(r.status_code, 200, r.content)
            order.refresh_from_db()
            self.assertEqual(order.status, "cancelled")
            self.assertEqual(self.w.post(f"/api/warehouse/orders/{order.id}/cancel/").status_code, 409)
        self.assertEqual(Order.objects.count(), 2)          # orders are kept, not deleted
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock, 9)
        self.assertIn("Damaged stock", self.cust.quickpack_notifications.latest("id").message)

    def test_warehouse_cannot_cancel_out_for_delivery_and_customer_cannot_use_warehouse_api(self):
        order = self.make("out_for_delivery")
        self.assertEqual(self.w.post(f"/api/warehouse/orders/{order.id}/cancel/").status_code, 409)
        order2 = self.make("placed")
        self.assertEqual(self.c.post(f"/api/warehouse/orders/{order2.id}/cancel/").status_code, 403)


class DeleteOrderTests(CancelOrderBothSidesTests):
    """'Delete order' on both sides: hidden from the list, the row stays in the database."""

    def test_customer_delete(self):
        placed, accepted, delivered = self.make("placed"), self.make("accepted"), self.make("delivered")
        self.assertEqual(self.c.post(f"/api/my-orders/{accepted.id}/delete/").status_code, 409)
        self.assertEqual(self.c.post(f"/api/my-orders/{placed.id}/delete/").status_code, 200)   # cancels + hides
        self.assertEqual(self.c.post(f"/api/my-orders/{delivered.id}/delete/").status_code, 200)
        self.assertEqual(self.o.post(f"/api/my-orders/{accepted.id}/delete/").status_code, 404)  # not Ravi's order
        left = [o["id"] for o in self.c.get("/api/my-orders/").json()["orders"]]
        self.assertEqual(left, [accepted.id])
        self.assertEqual(Order.objects.count(), 3)
        placed.refresh_from_db(); self.p.refresh_from_db()
        self.assertEqual((placed.status, self.p.stock), ("cancelled", 7))
        # warehouse still sees the delivered order the customer deleted
        ids = [o["id"] for o in self.w.get("/api/warehouse/dashboard/").json()["orders"]]
        self.assertIn(delivered.id, ids)

    def test_warehouse_delete(self):
        packed, out, delivered = self.make("packed"), self.make("out_for_delivery"), self.make("delivered")
        self.assertEqual(self.w.post(f"/api/warehouse/orders/{out.id}/delete/").status_code, 409)
        self.assertEqual(self.w.post(f"/api/warehouse/orders/{packed.id}/delete/").status_code, 200)
        self.assertEqual(self.w.post(f"/api/warehouse/orders/{delivered.id}/delete/").status_code, 200)
        self.assertEqual(self.c.post(f"/api/warehouse/orders/{out.id}/delete/").status_code, 403)
        ids = [o["id"] for o in self.w.get("/api/warehouse/dashboard/").json()["orders"]]
        self.assertEqual(ids, [out.id])
        self.assertEqual(Order.objects.count(), 3)
        self.assertIn("cancelled", self.cust.quickpack_notifications.latest("id").title)


import io
import tempfile
from django.test import override_settings


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ProductPhotoTests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name="Notebook", length=21, width=15, height=2, weight=0.3, stock=5)
        cust = User.objects.create_user("asha", password="Asha-pass-123")
        CustomerProfile.objects.get_or_create(user=cust)
        staff = User.objects.create_user("wh", password="Wh-pass-123")
        prof, _ = CustomerProfile.objects.get_or_create(user=staff)
        prof.role = "warehouse"
        prof.save()
        self.c, self.w = self.client_class(), self.client_class()
        self.c.login(username="asha", password="Asha-pass-123")
        self.w.login(username="wh", password="Wh-pass-123")

    def png(self, name="a.png"):
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        buf = io.BytesIO(); Image.new("RGB", (20, 20), "red").save(buf, "PNG")
        return SimpleUploadedFile(name, buf.getvalue(), content_type="image/png")

    def test_no_photo_by_default_and_existing_products_are_unchanged(self):
        self.assertIsNone(self.c.get("/api/products/").json()["products"][0]["image"])

    def test_warehouse_uploads_replaces_and_removes_photo(self):
        url = f"/api/products/{self.p.id}/image/"
        r = self.w.post(url, {"image": self.png()})
        self.assertEqual(r.status_code, 200, r.content)
        img = self.c.get("/api/products/").json()["products"][0]["image"]
        self.assertTrue(img and img.startswith("/media/products/"))
        self.assertEqual(self.w.post(url, {"image": self.png("b.png")}).status_code, 200)
        self.assertIsNone(self.w.post(url, {"remove": "1"}).json()["image"])

    def test_bad_uploads_and_permissions(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        url = f"/api/products/{self.p.id}/image/"
        self.assertEqual(self.c.post(url, {"image": self.png()}).status_code, 403)
        self.assertEqual(self.w.post(url, {"image": SimpleUploadedFile("x.png", b"not a picture")}).status_code, 400)
        self.assertEqual(self.w.post(url, {}).status_code, 400)
        self.assertEqual(self.w.post("/api/products/999/image/", {"image": self.png()}).status_code, 404)
