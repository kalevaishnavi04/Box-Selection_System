import json

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase

from .models import Order, OrderItem, Product, Recommendation
from .services import BoxSpec, Item, can_pack, recommend

SMALL = BoxSpec("Small", 20, 15, 10, 2, 10)
MEDIUM = BoxSpec("Medium", 30, 20, 15, 5, 18)
LARGE = BoxSpec("Large", 45, 35, 30, 15, 40)
BOXES = [LARGE, SMALL, MEDIUM]          # deliberately unsorted

EARPHONES = Item("Earphones", 12, 10, 5, 0.2)
NOTEBOOK = Item("Notebook", 21, 15, 2, 0.3)
BOTTLE = Item("Bottle", 25, 7, 7, 0.5)
DUMBBELL = Item("Dumbbell", 25, 10, 10, 4)
VASE = Item("Vase", 20, 12, 12, 0.8, fragile=True)


class RecommendLogicTests(SimpleTestCase):
    def test_empty_order(self):
        self.assertEqual(recommend([], BOXES)["status"], "empty")

    def test_tiny_item_gets_smallest_box(self):
        r = recommend([(EARPHONES, 1)], BOXES)
        self.assertEqual(r["boxes"][0]["box"], "Small")

    def test_real_life_ravi_order_gets_medium(self):
        r = recommend([(EARPHONES, 1), (NOTEBOOK, 1), (BOTTLE, 1)], BOXES)
        self.assertEqual(r["status"], "single_box")
        self.assertEqual(r["boxes"][0]["box"], "Medium")
        self.assertEqual(r["total_weight_kg"], 1.0)
        self.assertEqual(r["savings_vs_largest"], 22)
        self.assertIn("Small", [x["box"] for x in r["rejected"]])

    def test_rotation_is_allowed(self):
        # 8 x 2 x 25 only fits Medium if it is turned; sorted-dim check handles it.
        r = recommend([(Item("Pole", 8, 2, 25, 0.1), 1)], BOXES)
        self.assertEqual(r["boxes"][0]["box"], "Medium")

    def test_overweight_goes_to_bigger_box(self):
        r = recommend([(DUMBBELL, 2)], BOXES)            # 8 kg
        self.assertEqual(r["boxes"][0]["box"], "Large")

    def test_exact_fit_is_accepted(self):
        r = recommend([(Item("Block", 20, 15, 10, 2), 1)], BOXES)
        self.assertEqual(r["boxes"][0]["box"], "Small")

    def test_cheapest_wins_not_smallest(self):
        cheap_big = BoxSpec("CheapBig", 50, 40, 30, 20, 5)
        r = recommend([(EARPHONES, 1)], [SMALL, cheap_big])
        self.assertEqual(r["boxes"][0]["box"], "CheapBig")

    def test_tie_on_cost_prefers_smaller_volume(self):
        a = BoxSpec("A", 40, 40, 40, 10, 10)
        b = BoxSpec("B", 30, 30, 30, 10, 10)
        r = recommend([(EARPHONES, 1)], [a, b])
        self.assertEqual(r["boxes"][0]["box"], "B")

    def test_volume_ok_but_arrangement_impossible(self):
        # Two 11 cm cubes: total volume 2662 < box volume 2880, but 11+11 > 12 in every direction
        box = BoxSpec("Tight", 20, 12, 12, 10, 10)
        cube = Item("Cube", 11, 11, 11, 1)
        self.assertFalse(can_pack([cube, cube], box))
        r = recommend([(cube, 2)], [box], allow_split=False)
        self.assertEqual(r["status"], "no_fit")

    def test_many_small_items_pack_together(self):
        shirt = Item("Shirt", 25, 20, 2, 0.2)
        r = recommend([(shirt, 10)], BOXES)
        self.assertEqual(r["status"], "single_box")
        self.assertEqual(r["boxes"][0]["box"], "Large")

    def test_too_heavy_splits_into_multiple_boxes(self):
        r = recommend([(DUMBBELL, 4)], BOXES)            # 16 kg > 15 kg
        self.assertEqual(r["status"], "multi_box")
        self.assertGreater(len(r["boxes"]), 1)
        self.assertEqual(sum(b["items"]["Dumbbell"] for b in r["boxes"]), 4)
        self.assertEqual(r["total_cost"], sum(b["cost"] for b in r["boxes"]))

    def test_split_can_be_turned_off(self):
        r = recommend([(DUMBBELL, 4)], BOXES, allow_split=False)
        self.assertEqual(r["status"], "no_fit")

    def test_item_bigger_than_every_box(self):
        r = recommend([(Item("Ladder", 90, 10, 5, 3), 1)], BOXES)
        self.assertEqual(r["status"], "no_fit")
        self.assertIn("Ladder", r["message"])

    def test_fragile_not_packed_with_heavy(self):
        r = recommend([(VASE, 1), (DUMBBELL, 1)], BOXES)
        self.assertEqual(r["status"], "multi_box")
        for b in r["boxes"]:
            self.assertFalse("Vase" in b["items"] and "Dumbbell" in b["items"])

    def test_split_message_names_the_fragile_rule(self):
        r = recommend([(VASE, 1), (DUMBBELL, 1)], BOXES)
        self.assertIn("Fragile items cannot share a box", r["message"])
        r2 = recommend([(DUMBBELL, 4)], BOXES)
        self.assertIn("No single box fits", r2["message"])

    def test_fragile_with_light_items_is_fine(self):
        r = recommend([(VASE, 1), (NOTEBOOK, 1)], BOXES)
        self.assertEqual(r["status"], "single_box")

    def test_fill_percent_reported(self):
        r = recommend([(Item("Block", 20, 15, 10, 1), 1)], BOXES)
        self.assertEqual(r["boxes"][0]["fill_percent"], 100.0)

    def test_no_boxes_configured(self):
        self.assertEqual(recommend([(EARPHONES, 1)], [])["status"], "no_fit")


class ApiTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)
        self.p = {p.name: p.id for p in Product.objects.all()}

    def post(self, items, **extra):
        return self.client.post("/api/recommend-box/",
                                data=json.dumps({"items": items, **extra}),
                                content_type="application/json")

    def test_recommend_medium(self):
        r = self.post([{"product_id": self.p["Notebook"], "quantity": 1},
                       {"product_id": self.p["Water bottle"], "quantity": 1}])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["boxes"][0]["box"], "Medium")

    def test_request_is_saved_in_history(self):
        self.post([{"product_id": self.p["Phone case"], "quantity": 1}])
        self.assertEqual(Recommendation.objects.count(), 1)
        h = self.client.get("/api/history/").json()
        self.assertEqual(h["results"][0]["status"], "single_box")

    def test_empty_items_is_400(self):
        self.assertEqual(self.post([]).status_code, 400)

    def test_bad_json_is_400(self):
        r = self.client.post("/api/recommend-box/", data="nope", content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_zero_quantity_is_400(self):
        self.assertEqual(self.post([{"product_id": self.p["Notebook"], "quantity": 0}]).status_code, 400)

    def test_unknown_product_is_404(self):
        self.assertEqual(self.post([{"product_id": 9999, "quantity": 1}]).status_code, 404)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get("/api/recommend-box/").status_code, 405)

    def test_no_fit_is_422_when_split_disabled(self):
        r = self.post([{"product_id": self.p["Dumbbell"], "quantity": 4}], allow_split=False)
        self.assertEqual(r.status_code, 422)

    def test_order_endpoint(self):
        order = Order.objects.first()
        r = self.client.post(f"/api/orders/{order.id}/recommend-box/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["boxes"][0]["box"], "Medium")
        self.assertEqual(Recommendation.objects.first().order_id, order.id)

    def test_order_not_found(self):
        self.assertEqual(self.client.post("/api/orders/999/recommend-box/").status_code, 404)

    def test_seed_is_repeatable(self):
        call_command("seed_demo", verbosity=0)
        self.assertEqual(Product.objects.count(), 10)

    def test_home_page_loads_with_products(self):
        r = self.client.get("/packing/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Warehouse screen")


class CustomerWarehouseFlowTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)
        self.p = {p.name: p.id for p in Product.objects.all()}
        self.box = {b["name"]: b["id"] for b in self.client.get("/api/boxes/").json()["boxes"]}

    def place(self, items, name="Aarav"):
        return self.client.post("/api/orders/place/", json.dumps(
            {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
            content_type="application/json")

    def act(self, oid, action, body=None):
        return self.client.post(f"/api/orders/{oid}/{action}/", json.dumps(body or {}),
                                content_type="application/json")

    def pick_all(self, oid):
        order = next(o for o in self.client.get("/api/orders/").json()["orders"] if o["id"] == oid)
        for i in order["items"]:
            if not i["unavailable"]:
                self.act(oid, f"items/{i['id']}/pick", {"picked": i["quantity"]})

    def test_customer_places_order(self):
        r = self.place([("Pen", 2), ("Chocolate bar", 3)])
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["status"], "placed")
        self.assertEqual(r.json()["total_weight"], 0.34)

    def test_warehouse_sees_new_orders_and_customer_sees_own(self):
        oid = self.place([("Pen", 1)]).json()["id"]
        queue = self.client.get("/api/orders/?status=placed").json()["orders"]
        self.assertIn(oid, [o["id"] for o in queue])
        mine = self.client.get("/api/orders/?customer=Aarav").json()["orders"]
        self.assertEqual([o["id"] for o in mine], [oid])

    def test_full_flow_with_recommended_box(self):
        oid = self.place([("Pen", 1), ("Pencil box", 1), ("Chocolate bar", 2)]).json()["id"]
        self.assertEqual(self.act(oid, "accept").json()["status"], "accepted")
        rec = self.client.post(f"/api/orders/{oid}/recommend-box/").json()
        self.assertEqual(rec["boxes"][0]["box"], "Small")
        self.pick_all(oid)
        r = self.act(oid, "pack", {"box_ids": [rec["boxes"][0]["box_id"]]}).json()
        self.assertEqual(r["status"], "packed")
        self.assertEqual(r["extra_cost"], 0)

    def test_packer_picks_bigger_box_costs_extra(self):
        oid = self.place([("Pen", 1)]).json()["id"]
        self.act(oid, "accept")
        self.pick_all(oid)
        r = self.act(oid, "pack", {"box_ids": [self.box["Large"]]}).json()
        self.assertEqual(r["extra_cost"], 30)       # Large 40 - Small 10

    def test_packer_picks_box_that_is_too_small(self):
        oid = self.place([("Water bottle", 1)]).json()["id"]
        self.act(oid, "accept")
        self.pick_all(oid)
        r = self.act(oid, "pack", {"box_ids": [self.box["Small"]]})
        self.assertEqual(r.status_code, 422)
        self.assertIn("does not fit", r.json()["error"])
        self.assertEqual(self.client.get("/api/orders/?status=accepted").json()["orders"][0]["id"], oid)

    def test_cannot_pack_before_accept_or_accept_twice(self):
        oid = self.place([("Pen", 1)]).json()["id"]
        self.assertEqual(self.act(oid, "pack", {"box_ids": [self.box["Small"]]}).status_code, 409)
        self.act(oid, "accept")
        self.assertEqual(self.act(oid, "accept").status_code, 409)

    def test_bad_orders_rejected(self):
        self.assertEqual(self.place([]).status_code, 400)
        r = self.client.post("/api/orders/place/", json.dumps(
            {"items": [{"product_id": 9999, "quantity": 1}]}), content_type="application/json")
        self.assertEqual(r.status_code, 404)


class StockAndAddItemsTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)
        self.p = {p.name: p.id for p in Product.objects.all()}

    def post(self, path, body):
        return self.client.post(path, json.dumps(body), content_type="application/json")

    def order(self, name, q):
        return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})

    def stock(self, name):
        return Product.objects.get(name=name).stock

    def test_ordering_reduces_stock(self):
        self.order("Pen", 3)
        self.assertEqual(self.stock("Pen"), 22)

    def test_out_of_stock_item_cannot_be_ordered(self):
        r = self.order("Study table", 1)
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["error"], "Study table is out of stock")
        self.assertEqual(Order.objects.filter(customer_name="Aarav").count(), 0)

    def test_cannot_order_more_than_stock(self):
        r = self.order("Dumbbell", 7)
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["error"], "Only 6 Dumbbell left")
        self.assertEqual(self.stock("Dumbbell"), 6)

    def test_add_items_before_accept_merges_quantity(self):
        oid = self.order("Pen", 1).json()["id"]
        r = self.post(f"/api/orders/{oid}/add-items/", {"items": [
            {"product_id": self.p["Pen"], "quantity": 2}, {"product_id": self.p["Notebook"], "quantity": 1}]})
        self.assertEqual(r.status_code, 200)
        qty = {i["name"]: i["quantity"] for i in r.json()["items"]}
        self.assertEqual(qty, {"Pen": 3, "Notebook": 1})
        self.assertEqual(self.stock("Pen"), 22)

    def test_cannot_add_items_after_accept(self):
        oid = self.order("Pen", 1).json()["id"]
        self.post(f"/api/orders/{oid}/accept/", {})
        r = self.post(f"/api/orders/{oid}/add-items/", {"items": [{"product_id": self.p["Pen"], "quantity": 1}]})
        self.assertEqual(r.status_code, 409)

    def test_add_items_respects_stock(self):
        oid = self.order("Pen", 1).json()["id"]
        r = self.post(f"/api/orders/{oid}/add-items/", {"items": [{"product_id": self.p["Study table"], "quantity": 1}]})
        self.assertEqual(r.status_code, 409)

    def test_warehouse_adds_product_and_customer_can_order_it(self):
        r = self.post("/api/products/add/", {"name": "Stapler", "length": 12, "width": 5, "height": 5,
                                             "weight": 0.2, "stock": 10, "fragile": False})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.order_by_id(r.json()["id"]).status_code, 201)

    def order_by_id(self, pid):
        return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": pid, "quantity": 1}]})

    def test_add_product_validation(self):
        self.assertEqual(self.post("/api/products/add/", {"name": "", "length": 1, "width": 1, "height": 1, "weight": 1}).status_code, 400)
        self.assertEqual(self.post("/api/products/add/", {"name": "X", "length": 0, "width": 1, "height": 1, "weight": 1}).status_code, 400)
        self.assertEqual(self.post("/api/products/add/", {"name": "pen", "length": 1, "width": 1, "height": 1, "weight": 1}).status_code, 409)

    def test_restock_and_never_below_zero(self):
        pid = self.p["Study table"]
        self.assertEqual(self.post(f"/api/products/{pid}/stock/", {"change": 4}).json()["stock"], 4)
        self.assertEqual(self.post(f"/api/products/{pid}/stock/", {"change": -10}).json()["stock"], 0)


class StockAndInventoryTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)
        self.p = {p.name: p for p in Product.objects.all()}

    def post(self, url, body=None):
        return self.client.post(url, json.dumps(body or {}), content_type="application/json")

    def place(self, items, name="Aarav"):
        return self.post("/api/orders/place/", {"customer_name": name, "items": [
            {"product_id": self.p[n].id, "quantity": q} for n, q in items]})

    def stock(self, name):
        return Product.objects.get(name=name).stock

    def test_out_of_stock_item_cannot_be_ordered(self):
        r = self.place([("Study table", 1)])
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["unavailable"], ["Study table"])
        self.assertEqual(Order.objects.filter(customer_name="Aarav").count(), 0)

    def test_more_than_stock_is_refused_and_ordering_reduces_stock(self):
        self.assertEqual(self.place([("Pen", 26)]).status_code, 409)
        self.assertEqual(self.place([("Pen", 5)]).status_code, 201)
        self.assertEqual(self.stock("Pen"), 20)

    def test_cancel_returns_stock_only_before_accept(self):
        oid = self.place([("Pen", 5)]).json()["id"]
        self.assertEqual(self.post(f"/api/orders/{oid}/cancel/").json()["status"], "cancelled")
        self.assertEqual(self.stock("Pen"), 25)
        oid2 = self.place([("Pen", 1)]).json()["id"]
        self.post(f"/api/orders/{oid2}/accept/")
        self.assertEqual(self.post(f"/api/orders/{oid2}/cancel/").status_code, 409)

    def test_item_unavailable_is_removed_from_packing(self):
        o = self.place([("Pen", 1), ("Dumbbell", 1)]).json()
        self.post(f"/api/orders/{o['id']}/accept/")
        dumbbell = next(i for i in o["items"] if i["name"] == "Dumbbell")
        r = self.post(f"/api/orders/{o['id']}/items/{dumbbell['id']}/unavailable/").json()
        self.assertEqual(r["status"], "accepted")
        self.assertEqual(r["total_weight"], 0.02)
        self.assertEqual(self.stock("Dumbbell"), 0)
        rec = self.post(f"/api/orders/{o['id']}/recommend-box/").json()
        self.assertEqual(rec["boxes"][0]["box"], "Small")

    def test_order_cancelled_when_every_item_unavailable(self):
        o = self.place([("Pen", 1)]).json()
        r = self.post(f"/api/orders/{o['id']}/items/{o['items'][0]['id']}/unavailable/").json()
        self.assertEqual(r["status"], "cancelled")

    def test_warehouse_adds_product_and_restocks(self):
        r = self.post("/api/products/add/", {"name": "Eraser", "length": 4, "width": 2, "height": 1,
                                             "weight": 0.01, "stock": 50})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.place([("Pen", 1)]).status_code, 201)
        tid = self.p["Study table"].id
        self.assertEqual(self.post(f"/api/products/{tid}/stock/", {"add": 3}).json()["stock"], 3)
        self.assertEqual(self.place([("Study table", 1)]).status_code, 201)

    def test_add_product_validation(self):
        self.assertEqual(self.post("/api/products/add/", {"name": "", "length": 1, "width": 1,
                                                          "height": 1, "weight": 1}).status_code, 400)
        self.assertEqual(self.post("/api/products/add/", {"name": "X", "length": -1, "width": 1,
                                                          "height": 1, "weight": 1}).status_code, 400)


class ProductRequestTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)

    def post(self, url, body=None):
        return self.client.post(url, json.dumps(body or {}), content_type="application/json")

    def ask(self, name="Standing desk", qty=1, who="Aarav"):
        return self.post("/api/requests/place/", {"customer_name": who, "name": name, "quantity": qty})

    def review(self, rid, **body):
        return self.post(f"/api/requests/{rid}/review/", body)

    def test_request_does_not_add_product(self):
        before = Product.objects.count()
        r = self.ask()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["status"], "pending")
        self.assertEqual(Product.objects.count(), before)
        self.assertEqual(self.client.get("/api/requests/?customer=Aarav").json()["requests"][0]["name"], "Standing desk")

    def test_request_validation_and_duplicates(self):
        self.assertEqual(self.ask(name="  ").status_code, 400)
        self.assertEqual(self.ask(qty=0).status_code, 400)
        self.assertEqual(self.ask(name="pen").status_code, 409)          # already in shop
        self.ask()
        self.assertEqual(self.ask().status_code, 409)                    # already requested

    def test_approve_creates_orderable_product(self):
        rid = self.ask(qty=2).json()["id"]
        r = self.review(rid, decision="available", length=120, width=60, height=5, weight=15)
        self.assertEqual(r.json()["status"], "available")
        product = Product.objects.get(name="Standing desk")
        self.assertEqual(product.stock, 2)                               # defaults to requested quantity
        order = self.post("/api/orders/place/", {"customer_name": "Aarav",
                          "items": [{"product_id": product.id, "quantity": 1}]})
        self.assertEqual(order.status_code, 201)

    def test_approve_needs_size_and_weight(self):
        rid = self.ask().json()["id"]
        before = Product.objects.count()
        self.assertEqual(self.review(rid, decision="available", length=10).status_code, 400)
        self.assertEqual(self.review(rid, decision="available", length=0, width=1, height=1, weight=1).status_code, 400)
        self.assertEqual(Product.objects.count(), before)

    def test_temporarily_unavailable_needs_one_or_two_days_then_can_be_approved(self):
        rid = self.ask().json()["id"]
        self.assertEqual(self.review(rid, decision="temporarily_unavailable").status_code, 400)
        self.assertEqual(self.review(rid, decision="temporarily_unavailable", restock_days=5).status_code, 400)
        r = self.review(rid, decision="temporarily_unavailable", restock_days=2).json()
        self.assertEqual((r["status"], r["restock_days"]), ("temporarily_unavailable", 2))
        r = self.review(rid, decision="available", length=1, width=1, height=1, weight=1).json()
        self.assertEqual(r["status"], "available")
        self.assertIsNone(r["restock_days"])

    def test_not_available_is_final(self):
        rid = self.ask().json()["id"]
        r = self.review(rid, decision="not_available", reason="We do not handle furniture").json()
        self.assertEqual((r["status"], r["reason"]), ("not_available", "We do not handle furniture"))
        self.assertEqual(self.review(rid, decision="available", length=1, width=1, height=1, weight=1).status_code, 409)

    def test_bad_decision_and_unknown_request(self):
        rid = self.ask().json()["id"]
        self.assertEqual(self.review(rid, decision="maybe").status_code, 400)
        self.assertEqual(self.review(9999, decision="not_available").status_code, 404)

    def test_approve_when_product_name_already_exists(self):
        rid = self.ask(name="Stapler").json()["id"]
        self.post("/api/products/add/", {"name": "stapler", "length": 1, "width": 1, "height": 1, "weight": 1})
        r = self.review(rid, decision="available", length=1, width=1, height=1, weight=1)
        self.assertEqual(r.status_code, 409)


class PickingStepTests(TestCase):
    def setUp(self):
        call_command("seed_demo", verbosity=0)
        self.p = {p.name: p.id for p in Product.objects.all()}
        self.box = {b["name"]: b["id"] for b in self.client.get("/api/boxes/").json()["boxes"]}

    def post(self, url, body=None):
        return self.client.post(url, json.dumps(body or {}), content_type="application/json")

    def accepted_order(self, items):
        o = self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [
            {"product_id": self.p[n], "quantity": q} for n, q in items]}).json()
        self.post(f"/api/orders/{o['id']}/accept/")
        return o["id"], {i["name"]: i["id"] for i in o["items"]}

    def pick(self, oid, iid, n):
        return self.post(f"/api/orders/{oid}/items/{iid}/pick/", {"picked": n})

    def pack(self, oid):
        return self.post(f"/api/orders/{oid}/pack/", {"box_ids": [self.box["Small"]]})

    def test_cannot_pack_until_everything_is_picked(self):
        oid, ids = self.accepted_order([("Pen", 3), ("Pencil box", 1)])
        r = self.pack(oid)
        self.assertEqual(r.status_code, 409)
        self.assertIn("Pen (0 of 3)", r.json()["error"])
        self.pick(oid, ids["Pen"], 3)
        self.pick(oid, ids["Pencil box"], 1)
        self.assertEqual(self.pack(oid).json()["status"], "packed")

    def test_partly_picked_is_still_blocked(self):
        oid, ids = self.accepted_order([("Pen", 3)])
        order = self.pick(oid, ids["Pen"], 2).json()
        self.assertEqual(order["items"][0]["picked"], 2)
        self.assertEqual(self.pack(oid).status_code, 409)

    def test_pick_limits(self):
        oid, ids = self.accepted_order([("Pen", 3)])
        self.assertEqual(self.pick(oid, ids["Pen"], 4).status_code, 400)
        self.assertEqual(self.pick(oid, ids["Pen"], -1).status_code, 400)
        self.assertEqual(self.post(f"/api/orders/{oid}/items/{ids['Pen']}/pick/", {}).status_code, 400)
        self.assertEqual(self.pick(oid, 9999, 1).status_code, 404)

    def test_cannot_pick_before_accept(self):
        o = self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [
            {"product_id": self.p["Pen"], "quantity": 1}]}).json()
        self.assertEqual(self.pick(o["id"], o["items"][0]["id"], 1).status_code, 409)

    def test_unavailable_item_does_not_need_picking(self):
        oid, ids = self.accepted_order([("Pen", 1), ("Dumbbell", 1)])
        self.post(f"/api/orders/{oid}/items/{ids['Dumbbell']}/unavailable/")
        self.assertEqual(self.pick(oid, ids["Dumbbell"], 1).status_code, 409)
        self.pick(oid, ids["Pen"], 1)
        self.assertEqual(self.pack(oid).json()["status"], "packed")
