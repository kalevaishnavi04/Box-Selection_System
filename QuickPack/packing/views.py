import json
import re
from datetime import timedelta

from django.db import transaction
from django.db.models import F, Q
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Box, Order, OrderItem, Product, ProductRequest, Recommendation
from .services import check_box, expand, recommend

STATUS_CODE = {"single_box": 200, "multi_box": 200, "no_fit": 422, "empty": 400}


def _error(msg, status):
    return JsonResponse({"error": msg}, status=status)


def _run(entries, allow_split, order=None):
    """entries: [(product_id, quantity)]"""
    if not entries:
        return _error("Order has no items", 400)
    products = Product.objects.in_bulk([pid for pid, _ in entries])
    missing = sorted({pid for pid, _ in entries if pid not in products})
    if missing:
        return _error(f"Unknown product id(s): {missing}", 404)

    order_items = [(products[pid].to_item(), qty) for pid, qty in entries]
    # Create default boxes if no boxes are available
    if not Box.objects.exists():
        Box.objects.bulk_create([
            Box(name="Small", length=25, width=20, height=15,
                max_weight=3, cost=10),
            Box(name="Medium", length=40, width=30, height=25,
                max_weight=10, cost=18),
            Box(name="Large", length=60, width=45, height=40,
                max_weight=20, cost=30),
        ])

    boxes = [b.to_spec() for b in Box.objects.all()]
    result = recommend(order_items, boxes, allow_split=allow_split)

    Recommendation.objects.create(
        order=order,
        request_payload={"items": [{"product_id": p, "quantity": q} for p, q in entries],
                         "allow_split": allow_split},
        result=result, status=result["status"],
        total_cost=result["total_cost"] if result["boxes"] else None)
    return JsonResponse(result, status=STATUS_CODE[result["status"]])


@csrf_exempt
@require_POST
def recommend_box(request):
    try:
        data = json.loads(request.body or b"{}")
        raw = data["items"]
        entries = [(int(i["product_id"]), int(i["quantity"])) for i in raw]
        allow_split = bool(data.get("allow_split", True))
    except (ValueError, KeyError, TypeError):
        return _error('Send JSON like {"items": [{"product_id": 1, "quantity": 2}]}', 400)
    if any(q < 1 for _, q in entries):
        return _error("quantity must be at least 1", 400)
    return _run(entries, allow_split)


@csrf_exempt
@require_POST
def recommend_for_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return _error("Order not found", 404)
    entries = [(i.product_id, i.quantity) for i in order.items.filter(unavailable=False)]
    return _run(entries, True, order=order)


@require_GET
def history(request):
    rows = Recommendation.objects.all()[:20]
    return JsonResponse({"results": [
        {"id": r.id, "status": r.status, "total_cost": r.total_cost,
         "created_at": r.created_at.isoformat(), "request": r.request_payload,
         "message": r.result.get("message")} for r in rows]})


def _order_json(o):
    items = [{"id": i.id, "product_id": i.product_id, "name": i.product.name, "quantity": i.quantity,
              "weight": i.product.weight, "fragile": i.product.fragile, "unavailable": i.unavailable,
              "image": i.product.image.url if i.product.image else None,
              "picked": i.picked}
             for i in o.items.select_related("product")]
    ok = [i for i in items if not i["unavailable"]]
    return {"id": o.id, "customer": o.customer_name, "status": o.status, "items": items,
            "total_weight": round(sum(i["weight"] * i["quantity"] for i in ok), 3),
            "packed_boxes": o.packed_boxes, "created_at": o.created_at.isoformat()}


def _product_json(p):
    return {"id": p.id, "name": p.name, "length": p.length, "width": p.width, "height": p.height,
            "weight": p.weight, "fragile": p.fragile, "stock": p.stock,
            "image": p.image.url if p.image else None}


def _ensure_demo_shop_products():
    """Make the 12 demo shop items available on a fresh/empty database."""
    demo_products = [
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
    for name, length, width, height, weight, fragile, stock in demo_products:
        Product.objects.get_or_create(
            name=name,
            defaults={
                "length": length, "width": width, "height": height,
                "weight": weight, "fragile": fragile, "stock": stock,
            },
        )


@require_GET
def products(request):
    _ensure_demo_shop_products()
    return JsonResponse({"products": [_product_json(p) for p in Product.objects.order_by("id")]})


@csrf_exempt
@require_POST
def add_product(request):
    """Warehouse: add a new product to the catalogue."""
    try:
        d = json.loads(request.body or b"{}")
        name = str(d["name"]).strip()
        dims = [float(d[k]) for k in ("length", "width", "height", "weight")]
        stock = int(d.get("stock", 0))
    except (ValueError, KeyError, TypeError):
        return _error("Send name, length, width, height, weight (and stock)", 400)
    if not name or any(x <= 0 for x in dims) or stock < 0:
        return _error("Name is required; size and weight must be above 0", 400)
    if Product.objects.filter(name__iexact=name).exists():
        return _error(f"{name} already exists. Restock it instead", 409)
    p = Product.objects.create(name=name[:120], length=dims[0], width=dims[1], height=dims[2],
                               weight=dims[3], fragile=bool(d.get("fragile")), stock=stock)
    return JsonResponse(_product_json(p), status=201)


@csrf_exempt
@require_POST
def restock_product(request, product_id):
    """Warehouse: add (or remove) stock. Body: {"add": 10}"""
    try:
        p = Product.objects.get(pk=product_id)
        body = json.loads(request.body or b"{}")
        change = int(body["change"] if "change" in body else body["add"])
    except Product.DoesNotExist:
        return _error("Product not found", 404)
    except (ValueError, KeyError, TypeError):
        return _error('Send {"change": 10}', 400)
    p.stock = max(0, p.stock + change)
    p.save(update_fields=["stock"])
    return JsonResponse(_product_json(p))


@require_GET
def boxes(request):
    if not Box.objects.exists():
        Box.objects.bulk_create([
            Box(name="Small", length=25, width=20, height=15, max_weight=3, cost=10),
            Box(name="Medium", length=40, width=30, height=25, max_weight=10, cost=18),
            Box(name="Large", length=60, width=45, height=40, max_weight=20, cost=30),
        ])
    return JsonResponse({"boxes": [
        {"id": b.id, "name": b.name, "length": b.length, "width": b.width, "height": b.height,
         "max_weight": b.max_weight, "cost": b.cost} for b in Box.objects.order_by("cost")]})


def _take_stock(entries):
    """Check stock for [(product_id, qty)] and reduce it. Returns (products, error_response)."""
    found = Product.objects.in_bulk([p for p, _ in entries])
    if any(p not in found for p, _ in entries):
        return None, _error("Unknown product in order", 404)
    wanted = {}
    for pid, q in entries:
        wanted[pid] = wanted.get(pid, 0) + q
    problems = []
    for pid, q in wanted.items():
        p = found[pid]
        if p.stock == 0:
            problems.append((p.name, f"{p.name} is out of stock"))
        elif p.stock < q:
            problems.append((p.name, f"Only {p.stock} {p.name} left"))
    if problems:
        return None, JsonResponse({"error": "; ".join(m for _, m in problems),
                                   "unavailable": [n for n, _ in problems]}, status=409)
    for pid, q in wanted.items():
        found[pid].stock -= q
        found[pid].save(update_fields=["stock"])
    return found, None


@csrf_exempt
@require_POST
def place_order(request):
    """Customer app: place an order."""
    try:
        data = json.loads(request.body or b"{}")
        entries = [(int(i["product_id"]), int(i["quantity"])) for i in data["items"]]
        name = str(data.get("customer_name") or "Guest").strip()[:80] or "Guest"
    except (ValueError, KeyError, TypeError):
        return _error("Send customer_name and items", 400)
    if not entries or any(q < 1 for _, q in entries):
        return _error("Add at least one item (quantity 1 or more)", 400)
    with transaction.atomic():
        found, err = _take_stock(entries)
        if err:
            return err
        order = Order.objects.create(customer_name=name, customer=request.user if request.user.is_authenticated else None, delivery_address=str(data.get("delivery_address") or "")[:1000], delivery_phone=str(data.get("delivery_phone") or "")[:20], payment_status="cod" if data.get("payment_method") == "cod" else "pending")
        for pid, q in entries:
            OrderItem.objects.create(order=order, product=found[pid], quantity=q)
    _notify_warehouse(f"New order #{order.id}", f"{order.customer_name} placed a new order. Please review it.")
    return JsonResponse(_order_json(order), status=201)


@require_GET
def order_list(request):
    qs = Order.objects.order_by("-id")
    if request.GET.get("status"):
        qs = qs.filter(status__in=request.GET["status"].split(","))
    if request.GET.get("customer"):
        qs = qs.filter(customer_name=request.GET["customer"])
    return JsonResponse({"orders": [_order_json(o) for o in qs[:30]]})


@csrf_exempt
@require_POST
def accept_order(request, order_id):
    """Warehouse: accept an incoming order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return _error("Order not found", 404)
    if order.status != Order.PLACED:
        return _error(f"Order is already {order.status}", 409)
    order.status = Order.ACCEPTED
    order.save(update_fields=["status"])
    _notify_customer(order, f"Order #{order.id} accepted", "The warehouse accepted your order and will start packing it.")
    return JsonResponse(_order_json(order))


@csrf_exempt
@require_POST
def pack_order(request, order_id):
    """Warehouse: packer confirms which box(es) were used."""
    try:
        order = Order.objects.get(pk=order_id)
        box_ids = [int(b) for b in json.loads(request.body or b"{}")["box_ids"]]
    except Order.DoesNotExist:
        return _error("Order not found", 404)
    except (ValueError, KeyError, TypeError):
        return _error("Send box_ids as a list", 400)
    if order.status != Order.ACCEPTED:
        return _error("Accept the order before packing it", 409)
    not_picked = [f"{i.product.name} ({i.picked} of {i.quantity})"
                  for i in order.items.select_related("product").filter(unavailable=False)
                  if i.picked < i.quantity]
    if not_picked:
        return _error("Pick all items first: " + ", ".join(not_picked), 409)
    chosen = list(Box.objects.in_bulk(box_ids).values()) if box_ids else []
    if not box_ids or len({b.id for b in chosen}) != len(set(box_ids)):
        return _error("Pick at least one valid box", 400)
    by_id = {b.id: b for b in chosen}
    used = [by_id[i] for i in box_ids]

    order_items = [(i.product.to_item(), i.quantity)
                   for i in order.items.select_related("product").filter(unavailable=False)]
    if len(used) == 1:                       # we can verify a single-box choice
        ok, reason = check_box(expand(order_items), used[0].to_spec())
        if not ok:
            return _error(f"The {used[0].name} box cannot hold this order: {reason}", 422)
    rec = recommend(order_items, [b.to_spec() for b in Box.objects.all()])
    cost = sum(b.cost for b in used)
    order.packed_boxes = [{"box": b.name, "cost": b.cost} for b in used]
    order.status = Order.PACKED
    order.save(update_fields=["packed_boxes", "status"])
    _notify_customer(order, f"Order #{order.id} packed", "Your order has been packed and is getting ready for delivery.")
    return JsonResponse({**_order_json(order), "recommended_cost": rec["total_cost"],
                         "extra_cost": cost - rec["total_cost"]})


@csrf_exempt
@require_POST
def add_items(request, order_id):
    """Customer: add more items to an order the warehouse has not accepted yet."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return _error("Order not found", 404)
    try:
        entries = [(int(i["product_id"]), int(i["quantity"]))
                   for i in json.loads(request.body or b"{}")["items"]]
    except (ValueError, KeyError, TypeError):
        return _error("Send items", 400)
    if not entries or any(q < 1 for _, q in entries):
        return _error("Add at least one item (quantity 1 or more)", 400)
    if order.status != Order.PLACED:
        return _error("The warehouse already accepted this order, so items can no longer be added", 409)
    with transaction.atomic():
        found, err = _take_stock(entries)
        if err:
            return err
        for pid, q in entries:
            item, created = OrderItem.objects.get_or_create(order=order, product_id=pid, defaults={"quantity": q})
            if not created:
                item.quantity += q
                item.save(update_fields=["quantity"])
    return JsonResponse(_order_json(order))


def _cancel_and_restock(order):
    """Mark an order cancelled and put its (available) items back in stock. The order row is kept."""
    for i in order.items.select_related("product"):
        if not i.unavailable:
            i.product.stock += i.quantity
            i.product.save(update_fields=["stock"])
    order.status = Order.CANCELLED
    order.save(update_fields=["status"])


@csrf_exempt
@require_POST
def cancel_order(request, order_id):
    """Customer: cancel an order the warehouse has not accepted yet."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return _error("Order not found", 404)
    if request.user.is_authenticated and order.customer_id and order.customer_id != request.user.id:
        return _error("This is not your order", 403)
    if order.status != Order.PLACED:
        return _error("The warehouse already started this order, so it cannot be cancelled", 409)
    _cancel_and_restock(order)
    return JsonResponse(_order_json(order))


@csrf_exempt
@require_POST
def mark_unavailable(request, order_id, item_id):
    """Warehouse: this item cannot be supplied. The customer sees it removed."""
    try:
        order = Order.objects.get(pk=order_id)
        item = order.items.select_related("product").get(pk=item_id)
    except (Order.DoesNotExist, OrderItem.DoesNotExist):
        return _error("Order or item not found", 404)
    if order.status not in (Order.PLACED, Order.ACCEPTED):
        return _error("This order can no longer be changed", 409)
    item.unavailable = True
    item.save(update_fields=["unavailable"])
    item.product.stock = 0
    item.product.save(update_fields=["stock"])
    if not order.items.filter(unavailable=False).exists():
        order.status = Order.CANCELLED
        order.save(update_fields=["status"])
    _notify_customer(order, f"Order #{order.id} item update", f"{item.product.name} is unavailable. Your order has been updated.")
    if order.status == Order.CANCELLED:
        _notify_customer(order, f"Order #{order.id} cancelled", "No items were available, so the order was cancelled.")
    return JsonResponse(_order_json(order))


def _request_reply(r):
    """The message the warehouse 'sends back' to the customer for an item request."""
    if r.status == ProductRequest.AVAILABLE:
        return f"Good news! {r.name} is now available in the shop. You can order it."
    if r.status == ProductRequest.TEMPORARY:
        d = r.restock_days
        return f"{r.name} is not in stock right now. It will be available in {d} day{'s' if d != 1 else ''}."
    if r.status == ProductRequest.NOT_AVAILABLE:
        return f"Sorry, we cannot supply {r.name}." + (f" Reason: {r.reason}" if r.reason else "")
    return "The warehouse is checking your request."


def _request_json(r):
    return {"id": r.id, "customer": r.customer_name, "name": r.name, "quantity": r.quantity,
            "note": r.note, "status": r.status, "restock_days": r.restock_days,
            "reason": r.reason, "product_id": r.product_id, "reply": _request_reply(r),
            "created_at": r.created_at.isoformat()}


@csrf_exempt
@require_POST
def place_request(request):
    """Customer: ask for an item that is not in the shop. Nothing is added to the catalogue."""
    try:
        d = json.loads(request.body or b"{}")
        name = str(d["name"]).strip()
        quantity = int(d.get("quantity", 1))
        customer = str(d.get("customer_name") or "Guest").strip()[:80] or "Guest"
    except (ValueError, KeyError, TypeError):
        return _error("Send name and quantity", 400)
    if not name or quantity < 1:
        return _error("Give the item a name and a quantity of 1 or more", 400)
    if Product.objects.filter(name__iexact=name).exists():
        return _error(f"{name} is already in the shop. You can order it directly", 409)
    if ProductRequest.objects.filter(customer_name=customer, name__iexact=name,
                                     status__in=[ProductRequest.PENDING, ProductRequest.TEMPORARY]).exists():
        return _error(f"You already requested {name}", 409)
    user = request.user if request.user.is_authenticated else None
    if user:
        customer = (user.first_name or user.username)[:80]
    r = ProductRequest.objects.create(customer_name=customer, user=user, name=name[:120], quantity=quantity,
                                      note=str(d.get("note") or "")[:200])
    _notify_warehouse(f"New product request: {r.name}", f"{r.customer_name} requested {r.quantity} × {r.name}.")
    return JsonResponse(_request_json(r), status=201)


@require_GET
def request_list(request):
    qs = ProductRequest.objects.order_by("-id")
    if request.GET.get("customer"):
        qs = qs.filter(customer_name=request.GET["customer"])
    if request.GET.get("status"):
        qs = qs.filter(status__in=request.GET["status"].split(","))
    return JsonResponse({"requests": [_request_json(r) for r in qs[:30]]})


@csrf_exempt
@require_POST
def review_request(request, request_id):
    """Warehouse employee verifies a request: available | temporarily_unavailable | not_available."""
    try:
        r = ProductRequest.objects.get(pk=request_id)
        d = json.loads(request.body or b"{}")
        decision = d["decision"]
    except ProductRequest.DoesNotExist:
        return _error("Request not found", 404)
    except (ValueError, KeyError, TypeError):
        return _error("Send a decision", 400)
    if r.status not in (ProductRequest.PENDING, ProductRequest.TEMPORARY):
        return _error("This request was already decided", 409)

    if decision == ProductRequest.AVAILABLE:
        try:
            dims = [float(d[k]) for k in ("length", "width", "height", "weight")]
            stock = int(d.get("stock", r.quantity))
        except (ValueError, KeyError, TypeError):
            return _error("To approve, enter length, width, height and weight", 400)
        if any(x <= 0 for x in dims) or stock < 0:
            return _error("Size and weight must be above 0", 400)
        if Product.objects.filter(name__iexact=r.name).exists():
            return _error(f"{r.name} is already in the catalogue. Restock it instead", 409)
        r.product = Product.objects.create(name=r.name, length=dims[0], width=dims[1], height=dims[2],
                                           weight=dims[3], fragile=bool(d.get("fragile")), stock=stock)
        r.status, r.restock_days = ProductRequest.AVAILABLE, None
    elif decision == ProductRequest.TEMPORARY:
        if d.get("restock_days") not in (1, 2):
            return _error("Choose the expected restock time: 1 day or 2 days", 400)
        r.status, r.restock_days = ProductRequest.TEMPORARY, d["restock_days"]
    elif decision == ProductRequest.NOT_AVAILABLE:
        r.status, r.restock_days = ProductRequest.NOT_AVAILABLE, None
        r.reason = str(d.get("reason") or "")[:200]
    else:
        return _error("Decision must be available, temporarily_unavailable or not_available", 400)
    r.save()
    if r.user_id:
        UserNotification.objects.create(user=r.user, title=f"Your request: {r.name}", message=_request_reply(r)[:300])
    return JsonResponse(_request_json(r))


@csrf_exempt
@require_POST
def pick_item(request, order_id, item_id):
    """Warehouse: the packer says how many of this item were picked from the shelf."""
    try:
        order = Order.objects.get(pk=order_id)
        item = order.items.get(pk=item_id)
        picked = int(json.loads(request.body or b"{}")["picked"])
    except (Order.DoesNotExist, OrderItem.DoesNotExist):
        return _error("Order or item not found", 404)
    except (ValueError, KeyError, TypeError):
        return _error('Send {"picked": 2}', 400)
    if order.status != Order.ACCEPTED:
        return _error("Accept the order before picking items", 409)
    if item.unavailable:
        return _error("This item was marked not available", 409)
    if not 0 <= picked <= item.quantity:
        return _error(f"Pick between 0 and {item.quantity}", 400)
    item.picked = picked
    item.save(update_fields=["picked"])
    return JsonResponse(_order_json(order))


def index(request):
    return render(request, "packing/index.html")

# QuickPack customer and warehouse workspace APIs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from .models import CustomerProfile, WishlistItem, SupportTicket, UserNotification


def _body(request):
    try:
        return json.loads(request.body or b"{}")
    except (ValueError, TypeError):
        return None


@require_POST
def signup_api(request):
    d = _body(request)
    if d is None:
        return _error("Invalid JSON", 400)
    workspace = str(request.headers.get("X-Workspace", "customer")).lower()
    if workspace not in {"customer", "warehouse"}:
        return _error("Unknown workspace", 400)
    username = str(d.get("username") or d.get("email") or "").strip()
    email = str(d.get("email") or "").strip().lower()
    password = str(d.get("password") or "")
    if not username or len(password) < 8:
        return _error("Email/username and a password of at least 8 characters are required", 400)
    if User.objects.filter(username=username).exists() or (email and User.objects.filter(email=email).exists()):
        return _error("An account with these details already exists", 409)
    user = User.objects.create_user(username=username, email=email, password=password,
                                    first_name=str(d.get("name") or "")[:150])
    role = CustomerProfile.WAREHOUSE if workspace == "warehouse" else CustomerProfile.CUSTOMER
    CustomerProfile.objects.create(user=user, role=role, phone=str(d.get("phone") or "")[:20],
                                   address=str(d.get("address") or "")[:500])
    login(request, user)
    return JsonResponse({"message": "Warehouse account created" if workspace == "warehouse" else "Customer account created",
                         "username": user.username, "role": role}, status=201)


@require_POST
def login_api(request):
    d = _body(request)
    if d is None:
        return _error("Invalid JSON", 400)
    identity = str(d.get("username") or d.get("email") or "").strip()
    password = str(d.get("password") or "")
    user_obj = User.objects.filter(email__iexact=identity).first() if "@" in identity else None
    user = authenticate(request, username=(user_obj.username if user_obj else identity), password=password)
    if not user:
        return _error("Invalid username/email or password", 401)
    profile, _ = CustomerProfile.objects.get_or_create(user=user)
    workspace = str(request.headers.get("X-Workspace", "customer")).lower()
    if workspace == "warehouse":
        if not (user.is_staff or profile.role == CustomerProfile.WAREHOUSE):
            return _error("This account is not authorised for the warehouse. Use a warehouse staff account.", 403)
    elif workspace == "customer":
        if profile.role == CustomerProfile.WAREHOUSE:
            return _error("This is a warehouse account. Please sign in from the warehouse workspace.", 403)
    else:
        return _error("Unknown workspace", 400)
    login(request, user)
    return JsonResponse({"message": "Login successful", "username": user.username, "role": profile.role})


@require_POST
def logout_api(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@login_required
@require_http_methods(["GET", "POST"])
def account_api(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        d = _body(request) or {}
        request.user.first_name = str(d.get("name", request.user.first_name))[:150]
        request.user.email = str(d.get("email", request.user.email)).strip().lower()[:254]
        request.user.save(update_fields=["first_name", "email"])
        profile.phone = str(d.get("phone", profile.phone))[:20]
        profile.address = str(d.get("address", profile.address))[:1000]
        if d.get("payment_preference") in {"cod", "upi", "card"}:
            profile.payment_preference = d["payment_preference"]
        profile.save()
    return JsonResponse({"username": request.user.username, "name": request.user.first_name,
                         "email": request.user.email, "role": profile.role, "phone": profile.phone,
                         "address": profile.address, "payment_preference": profile.payment_preference,
                         "notifications_enabled": profile.notifications_enabled, "is_staff": request.user.is_staff})


@login_required
@require_http_methods(["GET", "POST"])
def wishlist_api(request):
    if request.method == "GET":
        rows = WishlistItem.objects.filter(user=request.user).select_related("product")
        return JsonResponse({"wishlist": [{"id": x.product_id, "name": x.product.name,
            "stock": x.product.stock, "weight": x.product.weight,
            "image": x.product.image.url if x.product.image else None} for x in rows]})
    d = _body(request)
    try:
        product = Product.objects.get(pk=int(d["product_id"]))
    except (TypeError, ValueError, KeyError, Product.DoesNotExist):
        return _error("Valid product_id is required", 400)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return JsonResponse({"message": "Added to wishlist"}, status=201)


@login_required
@require_POST
def wishlist_remove_api(request, product_id):
    WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({"message": "Removed from wishlist"})


@login_required
@require_GET
def my_requests_api(request):
    rows = ProductRequest.objects.filter(user=request.user).order_by("-id")[:50]
    return JsonResponse({"requests": [_request_json(r) for r in rows]})


@login_required
@require_http_methods(["GET", "POST"])
def support_api(request):
    if request.method == "GET":
        rows = SupportTicket.objects.filter(user=request.user).order_by("-created_at")
        return JsonResponse({"tickets": [{"id": t.id, "subject": t.subject, "message": t.message,
            "status": t.status, "reply": t.staff_reply, "order_id": t.order_id,
            "created_at": t.created_at.isoformat(), "updated_at": t.updated_at.isoformat()} for t in rows]})
    d = _body(request)
    subject, message = str(d.get("subject") or "").strip(), str(d.get("message") or "").strip()
    if not subject or not message:
        return _error("Subject and message are required", 400)
    order = None
    if d.get("order_id"):
        order = Order.objects.filter(pk=d["order_id"], customer=request.user).first()
        if not order:
            return _error("Order not found for this account", 404)
    t = SupportTicket.objects.create(user=request.user, order=order, subject=subject[:120], message=message)
    _notify_warehouse(f"New customer message: {t.subject}", f"{request.user.first_name or request.user.username}: {t.message}")
    return JsonResponse({"id": t.id, "status": t.status, "message": "Support ticket created"}, status=201)


@login_required
@require_http_methods(["GET", "POST"])
def notifications_api(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        d = _body(request)
        profile.notifications_enabled = bool(d.get("enabled", True))
        profile.save(update_fields=["notifications_enabled"])
        return JsonResponse({"notifications_enabled": profile.notifications_enabled, "is_staff": request.user.is_staff})
    rows = UserNotification.objects.filter(user=request.user).order_by("-created_at")[:50]
    return JsonResponse({"enabled": profile.notifications_enabled, "notifications": [
        {"id": n.id, "title": n.title, "message": n.message, "read": n.is_read,
         "created_at": n.created_at.isoformat()} for n in rows]})


@login_required
def my_orders_api(request):
    rows = Order.objects.filter(customer=request.user, hidden_for_customer=False).order_by("-created_at")
    return JsonResponse({"orders": [{"id": o.id, "status": o.status, "payment_status": o.payment_status,
        "delivery_address": o.delivery_address, "delivery_phone": o.delivery_phone,
        "delivery_person": o.delivery_person, "delivery_person_phone": o.delivery_person_phone,
        "delivery_latitude": str(o.delivery_latitude) if o.delivery_latitude is not None else None,
        "delivery_longitude": str(o.delivery_longitude) if o.delivery_longitude is not None else None,
        "delivery_location_updated_at": o.delivery_location_updated_at.isoformat() if o.delivery_location_updated_at else None,
        "estimated_delivery": o.estimated_delivery.isoformat() if o.estimated_delivery else None,
        "created_at": o.created_at.isoformat(), "packed_boxes": o.packed_boxes,
        "can_cancel": o.status == Order.PLACED, "can_delete": True,
        "items": [{"name": i.product.name, "quantity": i.quantity, "unavailable": i.unavailable}
                  for i in o.items.select_related("product")]} for o in rows]})


def _warehouse_required(request):
    if not request.user.is_authenticated:
        return _error("Login required", 401)
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if not (request.user.is_staff or profile.role == CustomerProfile.WAREHOUSE):
        return _error("Warehouse staff access required", 403)
    return None


@login_required
@require_GET
def warehouse_dashboard_api(request):
    denied = _warehouse_required(request)
    if denied:
        return denied
    rows = Order.objects.filter(hidden_for_warehouse=False).order_by("created_at")[:100]
    return JsonResponse({"orders": [{"id": o.id, "customer": o.customer_name, "status": o.status,
        "address": o.delivery_address, "phone": o.delivery_phone, "delivery_person": o.delivery_person,
        "delivery_person_phone": o.delivery_person_phone, "estimated_delivery": o.estimated_delivery.isoformat() if o.estimated_delivery else None}
        for o in rows], "low_stock": list(Product.objects.filter(stock__lte=5).values("id", "name", "stock")),
        "item_requests": [_request_json(r) for r in ProductRequest.objects.order_by("-id")[:100]],
        "tickets": [{"id": t.id, "customer": t.user.first_name or t.user.username, "subject": t.subject,
                     "message": t.message, "status": t.status, "reply": t.staff_reply, "order_id": t.order_id}
                    for t in SupportTicket.objects.select_related("user").order_by("-created_at")[:100]],
        "notifications": [{"id": n.id, "title": n.title, "message": n.message, "created_at": n.created_at.isoformat()}
                          for n in UserNotification.objects.filter(user=request.user).order_by("-created_at")[:30]]})


@login_required
@require_POST
def warehouse_delivery_update_api(request, order_id):
    denied = _warehouse_required(request)
    if denied:
        return denied
    d = _body(request)
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return _error("Order not found", 404)
    previous_status = order.status
    order.delivery_person = str(d.get("delivery_person") or order.delivery_person)[:80]
    order.delivery_person_phone = str(d.get("delivery_person_phone") or order.delivery_person_phone)[:20]
    order.delivery_address = str(d.get("delivery_address") or order.delivery_address)[:1000]
    order.delivery_phone = str(d.get("delivery_phone") or order.delivery_phone)[:20]
    eta = parse_datetime(d.get("estimated_delivery", "")) if d.get("estimated_delivery") else None
    if d.get("estimated_delivery") and not eta:
        return _error("estimated_delivery must be an ISO date/time", 400)
    if eta:
        order.estimated_delivery = eta
    try:
        if d.get("latitude") not in (None, ""):
            order.delivery_latitude = float(d["latitude"])
        if d.get("longitude") not in (None, ""):
            order.delivery_longitude = float(d["longitude"])
    except (TypeError, ValueError):
        return _error("Location coordinates must be numeric", 400)
    if d.get("status") in dict(Order.STATUSES):
        order.status = d["status"]
    order.save()
    _status_notification(order, previous_status)
    if order.customer_id and (d.get("latitude") not in (None, "") or d.get("longitude") not in (None, "")):
        _notify_customer(order, f"Order #{order.id} location updated", "The delivery location was updated. Open My Orders to view it on the map.")
    return JsonResponse({"message": "Delivery details updated", "order_id": order.id,
                         "status": order.status, "estimated_delivery": order.estimated_delivery.isoformat() if order.estimated_delivery else None})





@login_required
@require_POST
def warehouse_location_update_api(request, order_id):
    """Accept a fresh GPS coordinate from the delivery device without changing order status."""
    denied = _warehouse_required(request)
    if denied:
        return denied
    d = _body(request)
    if not isinstance(d, dict):
        return _error("Send latitude and longitude", 400)
    try:
        lat, lon = float(d.get("latitude")), float(d.get("longitude"))
    except (TypeError, ValueError):
        return _error("Location coordinates must be numeric", 400)
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return _error("Location coordinates are outside the valid range", 400)
    order = Order.objects.filter(pk=order_id).first()
    if not order:
        return _error("Order not found", 404)
    if order.status != Order.OUT:
        return _error("Live location can be shared only while the order is out for delivery", 409)
    order.delivery_latitude = lat
    order.delivery_longitude = lon
    order.delivery_location_updated_at = timezone.now()
    order.save(update_fields=["delivery_latitude", "delivery_longitude", "delivery_location_updated_at"])
    return JsonResponse({"message": "Live location updated", "order_id": order.id,
                         "latitude": str(order.delivery_latitude), "longitude": str(order.delivery_longitude),
                         "updated_at": order.delivery_location_updated_at.isoformat()})


_PHONE_OK = re.compile(r"^\+?\d{10,13}$")


def _notify_customer(order, title, message):
    """Persist an in-app notification for the account that owns this order."""
    if order.customer_id:
        UserNotification.objects.create(user=order.customer, title=title[:120], message=message[:300])


def _notify_warehouse(title, message):
    """Notify every active warehouse account; dashboard polling makes new work visible."""
    users = User.objects.filter(is_active=True).filter(
        Q(is_staff=True) | Q(customer_profile__role=CustomerProfile.WAREHOUSE)
    ).distinct()
    for user in users:
        UserNotification.objects.create(user=user, title=title[:120], message=message[:300])


def _status_notification(order, old_status=None):
    """Send a customer-facing update whenever an order changes state."""
    labels = dict(Order.STATUSES)
    if old_status == order.status:
        return
    _notify_customer(order, f"Order #{order.id}: {labels.get(order.status, order.status)}",
                     f"Your order status is now {labels.get(order.status, order.status)}.")


@login_required
@require_POST
def warehouse_send_order_api(request, order_id):
    """Last warehouse step: a PACKED order is handed to a delivery person and leaves the warehouse.
    Body: {"delivery_person": "Ramesh", "delivery_person_phone": "9876543210", "eta_minutes": 30}"""
    denied = _warehouse_required(request)
    if denied:
        return denied
    d = _body(request)
    if not isinstance(d, dict):
        return _error("Send JSON", 400)
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(pk=order_id)
        except Order.DoesNotExist:
            return _error("Order not found", 404)
        if order.status != Order.PACKED:
            return _error("Pack the order before sending it out", 409)
        person = str(d.get("delivery_person") or order.delivery_person).strip()[:80]
        phone = str(d.get("delivery_person_phone") or order.delivery_person_phone).strip()
        if not person or not _PHONE_OK.match(phone):
            return _error("Enter the delivery person's name and a valid mobile number", 400)
        try:
            minutes = int(d.get("eta_minutes") or 30)
        except (TypeError, ValueError):
            return _error("Delivery time must be a number of minutes", 400)
        if not 5 <= minutes <= 480:
            return _error("Delivery time must be between 5 and 480 minutes", 400)
        order.delivery_person, order.delivery_person_phone = person, phone
        order.estimated_delivery = timezone.now() + timedelta(minutes=minutes)
        order.status = Order.OUT
        order.save()
    _notify_customer(order, f"Order #{order.id} is on the way",
                     f"{person} ({phone}) will deliver it in about {minutes} minutes.")
    return JsonResponse({"message": "Order sent for delivery", "order_id": order.id, "status": order.status,
                         "estimated_delivery": order.estimated_delivery.isoformat()})


@login_required
@require_POST
def my_order_delete_api(request, order_id):
    """Customer: delete an order from my list. Not yet accepted -> it is cancelled first (stock returns).
    Being packed / on the way -> refused. The row is kept in the database (hidden), never erased."""
    with transaction.atomic():
        order = Order.objects.select_for_update().filter(pk=order_id, customer=request.user).first()
        if not order:
            return _error("Order not found", 404)
        if order.status in (Order.ACCEPTED, Order.PACKED, Order.OUT):
            return _error("The warehouse is already processing this order. You can delete it once it is delivered or cancelled.", 409)
        if order.status == Order.PLACED:
            _cancel_and_restock(order)
        order.hidden_for_customer = True
        order.save(update_fields=["hidden_for_customer"])
    return JsonResponse({"message": "Order deleted", "order_id": order.id})


@login_required
@require_POST
def warehouse_delete_order_api(request, order_id):
    """Warehouse: delete an order from the warehouse list. Placed / accepted / packed -> cancelled first
    (stock returns, customer is told). Out for delivery -> refused. The row is kept (hidden)."""
    denied = _warehouse_required(request)
    if denied:
        return denied
    cancelled = False
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(pk=order_id)
        except Order.DoesNotExist:
            return _error("Order not found", 404)
        if order.status == Order.OUT:
            return _error("This order is out for delivery. Mark it delivered before deleting it.", 409)
        if order.status in (Order.PLACED, Order.ACCEPTED, Order.PACKED):
            _cancel_and_restock(order)
            cancelled = True
        order.hidden_for_warehouse = True
        order.save(update_fields=["hidden_for_warehouse"])
    if cancelled:
        _notify_customer(order, f"Order #{order.id} cancelled", "The warehouse cancelled your order.")
    return JsonResponse({"message": "Order deleted", "order_id": order.id})


@login_required
@require_POST
def warehouse_cancel_order_api(request, order_id):
    """Warehouse: cancel an order that has not left the warehouse yet (placed / accepted / packed).
    The order is kept (status = cancelled), stock goes back, the customer is told. Body: {"reason": "..."}"""
    denied = _warehouse_required(request)
    if denied:
        return denied
    reason = str((_body(request) or {}).get("reason") or "").strip()[:150]
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(pk=order_id)
        except Order.DoesNotExist:
            return _error("Order not found", 404)
        if order.status not in (Order.PLACED, Order.ACCEPTED, Order.PACKED):
            return _error("This order is already cancelled, on its way or delivered, so it cannot be cancelled", 409)
        _cancel_and_restock(order)
    _notify_customer(order, f"Order #{order.id} cancelled",
                     "The warehouse cancelled your order." + (f" Reason: {reason}" if reason else ""))
    return JsonResponse({"message": "Order cancelled", "order_id": order.id, "status": order.status})


@login_required
@require_POST
def warehouse_deliver_order_api(request, order_id):
    denied = _warehouse_required(request)
    if denied:
        return denied
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(pk=order_id)
        except Order.DoesNotExist:
            return _error("Order not found", 404)
        if order.status != Order.OUT:
            return _error("Only an order that is out for delivery can be marked delivered", 409)
        order.status = Order.DELIVERED
        order.save(update_fields=["status"])
    _notify_customer(order, f"Order #{order.id} delivered", "Your order was delivered. Enjoy!")
    return JsonResponse({"message": "Marked delivered", "order_id": order.id, "status": order.status})


@login_required
@require_POST
def warehouse_ticket_reply_api(request, ticket_id):
    denied = _warehouse_required(request)
    if denied:
        return denied
    d = _body(request) or {}
    ticket = SupportTicket.objects.filter(pk=ticket_id).first()
    if not ticket:
        return _error("Support ticket not found", 404)
    reply = str(d.get("reply") or "").strip()[:3000]
    if not reply:
        return _error("Write a reply message for the customer first", 400)
    ticket.staff_reply = reply
    ticket.status = d.get("status") if d.get("status") in dict(SupportTicket.STATUSES) else SupportTicket.IN_PROGRESS
    ticket.save(update_fields=["staff_reply", "status", "updated_at"])
    UserNotification.objects.create(user=ticket.user, title=f"Reply to your message: {ticket.subject}"[:120],
                                    message=f"Warehouse: {reply}"[:300])
    return JsonResponse({"message": "Reply sent", "ticket_id": ticket.id})


MAX_IMAGE_BYTES = 3 * 1024 * 1024


@login_required
@require_POST
def product_image_api(request, product_id):
    """Warehouse: upload (multipart field "image") or remove (field "remove"=1) a product photo."""
    denied = _warehouse_required(request)
    if denied:
        return denied
    try:
        p = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return _error("Product not found", 404)
    if request.POST.get("remove"):
        if p.image:
            p.image.delete(save=False)
        p.image = None
        p.save(update_fields=["image"])
        return JsonResponse(_product_json(p))
    f = request.FILES.get("image")
    if not f:
        return _error("Choose a photo to upload", 400)
    if f.size > MAX_IMAGE_BYTES:
        return _error("Photo is too big. Please use one under 3 MB", 400)
    from PIL import Image
    try:
        img = Image.open(f)
        fmt = img.format
        img.verify()
    except Exception:
        return _error("That file is not a valid picture", 400)
    if fmt not in ("JPEG", "PNG", "WEBP"):
        return _error("Use a JPG, PNG or WEBP photo", 400)
    f.seek(0)
    if p.image:
        p.image.delete(save=False)
    ext = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[fmt]
    p.image.save(f"product-{p.id}.{ext}", f, save=True)
    return JsonResponse(_product_json(p))


def customer_workspace(request):
    return render(request, "packing/workspace.html", {"workspace": "customer"})


def warehouse_workspace(request):
    return render(request, "packing/workspace.html", {"workspace": "warehouse"})


def login_page(request):
    """Customer sign-in page."""
    from django.contrib import messages
    from django.shortcuts import redirect
    workspace = "customer"
    if request.user.is_authenticated:
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        if profile.role == CustomerProfile.WAREHOUSE or request.user.is_staff:
            messages.error(request, "This is a warehouse account. Please use Warehouse sign in.")
        else:
            return redirect('customer-workspace')
    if request.method == 'POST':
        identity = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        user_obj = User.objects.filter(email__iexact=identity).first() if '@' in identity else None
        user = authenticate(request, username=user_obj.username if user_obj else identity, password=password)
        if user is not None:
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
            if profile.role == CustomerProfile.WAREHOUSE and not user.is_staff:
                messages.error(request, 'This is a warehouse account. Please use Warehouse sign in.')
            else:
                login(request, user)
                return redirect('customer-workspace')
        else:
            messages.error(request, 'Incorrect email/username or password. Please try again.')
    return render(request, 'packing/auth.html', {'page_mode': 'login', 'workspace': workspace})


def signup_page(request):
    """Customer registration page."""
    from django.contrib import messages
    from django.shortcuts import redirect
    workspace = "customer"
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()[:150]
        email = (request.POST.get('email') or '').strip().lower()
        phone = (request.POST.get('phone') or '').strip()[:20]
        password = request.POST.get('password') or ''
        confirm = request.POST.get('confirm_password') or ''
        username = email
        if not name or not email or not password:
            messages.error(request, 'Please complete all required fields.')
        elif len(password) < 8:
            messages.error(request, 'Password must contain at least 8 characters.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists() or User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists. Please sign in.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
            CustomerProfile.objects.create(user=user, phone=phone, role=CustomerProfile.CUSTOMER)
            login(request, user)
            return redirect('customer-workspace')
    return render(request, 'packing/auth.html', {'page_mode': 'signup', 'workspace': workspace})


def warehouse_login_page(request):
    """Warehouse sign-in page, with its own session cookie."""
    from django.contrib import messages
    from django.shortcuts import redirect
    if request.user.is_authenticated:
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        if profile.role == CustomerProfile.WAREHOUSE or request.user.is_staff:
            return redirect('warehouse-workspace')
    if request.method == 'POST':
        identity = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        user_obj = User.objects.filter(email__iexact=identity).first() if '@' in identity else None
        user = authenticate(request, username=user_obj.username if user_obj else identity, password=password)
        if user is not None:
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
            if profile.role == CustomerProfile.WAREHOUSE or user.is_staff:
                login(request, user)
                return redirect('warehouse-workspace')
            messages.error(request, 'This is a customer account. Please use Customer sign in.')
        else:
            messages.error(request, 'Incorrect email/username or password. Please try again.')
    return render(request, 'packing/auth.html', {'page_mode': 'login', 'workspace': 'warehouse'})


def warehouse_signup_page(request):
    """Self-service warehouse registration page."""
    from django.contrib import messages
    from django.shortcuts import redirect
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()[:150]
        email = (request.POST.get('email') or '').strip().lower()
        phone = (request.POST.get('phone') or '').strip()[:20]
        password = request.POST.get('password') or ''
        confirm = request.POST.get('confirm_password') or ''
        if not name or not email or not password:
            messages.error(request, 'Please complete all required fields.')
        elif len(password) < 8:
            messages.error(request, 'Password must contain at least 8 characters.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=email).exists() or User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists. Please sign in.')
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            CustomerProfile.objects.create(user=user, phone=phone, role=CustomerProfile.WAREHOUSE)
            login(request, user)
            return redirect('warehouse-workspace')
    return render(request, 'packing/auth.html', {'page_mode': 'signup', 'workspace': 'warehouse'})

def logout_page(request):
    from django.shortcuts import redirect
    if request.method == 'POST':
        logout(request)
    return redirect('warehouse-login-page' if request.path.startswith('/warehouse/') else 'login-page')
