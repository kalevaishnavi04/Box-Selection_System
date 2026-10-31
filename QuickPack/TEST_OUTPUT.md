Hello,

I have completed and submitted the assignment within the given 24-hour deadline.

During testing, I ran 88 test cases, out of which 56 passed, 7 failed, and 25 encountered errors.

Due to the limited time, I could not resolve all the issues before submission. However, I have identified the issues and I am actively working on fixing them.

I apologize for the incomplete test results and appreciate your understanding.

Thank you for giving me this opportunity.

Regards,
Vaishnavi Manik Kale


==========================================================================
SETUP AND RUN LOG  (QuickPack)
==========================================================================

Microsoft Windows [Version 10.0.26200.9711]
(c) Microsoft Corporation. All rights reserved.

C:\Users\vaish\Downloads\Box_Selection>cd QuickPack

C:\Users\vaish\Downloads\Box_Selection\QuickPack>python -m venv venv

C:\Users\vaish\Downloads\Box_Selection\QuickPack>venv\Scripts\activate

(venv) C:\Users\vaish\Downloads\Box_Selection\QuickPack>pip install -r requirements.txt
Collecting Django>=5.0 (from -r requirements.txt (line 1))
  Using cached django-5.2.18-py3-none-any.whl.metadata (4.1 kB)
Collecting Pillow>=10.0 (from -r requirements.txt (line 2))
  Using cached pillow-13.0.0-cp311-cp311-win_amd64.whl.metadata (9.3 kB)
Collecting asgiref>=3.8.1 (from Django>=5.0->-r requirements.txt (line 1))
  Using cached asgiref-3.13.0-py3-none-any.whl.metadata (12 kB)
Collecting sqlparse>=0.3.1 (from Django>=5.0->-r requirements.txt (line 1))
  Using cached sqlparse-0.6.0-py3-none-any.whl.metadata (6.0 kB)
Collecting tzdata (from Django>=5.0->-r requirements.txt (line 1))
  Using cached tzdata-2026.6-py2.py3-none-any.whl.metadata (1.4 kB)
Using cached django-5.2.18-py3-none-any.whl (8.3 MB)
Using cached pillow-13.0.0-cp311-cp311-win_amd64.whl (7.3 MB)
Using cached asgiref-3.13.0-py3-none-any.whl (27 kB)
Using cached sqlparse-0.6.0-py3-none-any.whl (50 kB)
Using cached tzdata-2026.6-py2.py3-none-any.whl (348 kB)
Installing collected packages: tzdata, sqlparse, Pillow, asgiref, Django
Successfully installed Django-5.2.18 Pillow-13.0.0 asgiref-3.13.0 sqlparse-0.6.0 tzdata-2026.6

[notice] A new release of pip is available: 24.0 -> 26.2.2
[notice] To update, run: python.exe -m pip install --upgrade pip

(venv) C:\Users\vaish\Downloads\Box_Selection\QuickPack>python manage.py migrate
System check identified some issues:

WARNINGS:
packing.Box: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.CustomerProfile: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Order: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.OrderItem: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Product: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.ProductRequest: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Recommendation: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.SupportTicket: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.UserNotification: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.WishlistItem: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, packing, sessions
Running migrations:
  No migrations to apply.

(venv) C:\Users\vaish\Downloads\Box_Selection\QuickPack>python manage.py seed_demo
System check identified some issues:

WARNINGS:
packing.Box: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.CustomerProfile: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Order: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.OrderItem: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Product: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.ProductRequest: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Recommendation: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.SupportTicket: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.UserNotification: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.WishlistItem: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
QuickPack demo catalogue loaded: 12 shop products.

(venv) C:\Users\vaish\Downloads\Box_Selection\QuickPack>python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified some issues:

WARNINGS:
packing.Box: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.CustomerProfile: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Order: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.OrderItem: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Product: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.ProductRequest: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.Recommendation: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.SupportTicket: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.UserNotification: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
packing.WishlistItem: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PackingConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.

System check identified 10 issues (0 silenced).
October 31, 2026 - 15:16:39
Django version 5.2.18, using settings 'boxsystem.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.


==========================================================================
TEST OUTPUT  (QuickPack - python manage.py test -v 2)
==========================================================================

test_warehouse_cannot_cancel_out_for_delivery_and_customer_cannot_use_warehouse_api (packing.tests_send.CancelOrderBothSidesTests...) ... ok
test_customer_cancels_own_placed_order_and_stock_returns (packing.tests_send.DeleteOrderTests.test_customer_cancels_own_placed_order_and_stock_returns) ... ok
test_customer_cannot_cancel_after_accept (packing.tests_send.DeleteOrderTests.test_customer_cannot_cancel_after_accept) ... ok
test_customer_delete (packing.tests_send.DeleteOrderTests.test_customer_delete) ... ok
test_warehouse_cancels_accepted_or_packed_order_and_customer_is_told (packing.tests_send.DeleteOrderTests.test_warehouse_cancels_accepted_or_packed_order_and_customer_is_told) ... ok
test_warehouse_cannot_cancel_out_for_delivery_and_customer_cannot_use_warehouse_api (packing.tests_send.DeleteOrderTests.test_warehouse_cannot_cancel_out_for_delivery_and_customer_cannot_use_warehouse_api) ... ok
test_warehouse_delete (packing.tests_send.DeleteOrderTests.test_warehouse_delete) ... ok
test_bad_uploads_and_permissions (packing.tests_send.ProductPhotoTests.test_bad_uploads_and_permissions) ... ok
test_no_photo_by_default_and_existing_products_are_unchanged (packing.tests_send.ProductPhotoTests.test_no_photo_by_default_and_existing_products_are_unchanged) ... ok
test_warehouse_uploads_replaces_and_removes_photo (packing.tests_send.ProductPhotoTests.test_warehouse_uploads_replaces_and_removes_photo) ... ok
test_cannot_send_an_order_that_is_not_packed (packing.tests_send.SendOrderTests.test_cannot_send_an_order_that_is_not_packed) ... ok
test_needs_warehouse_login (packing.tests_send.SendOrderTests.test_needs_warehouse_login) ... ok
test_send_then_deliver_notifies_customer (packing.tests_send.SendOrderTests.test_send_then_deliver_notifies_customer) ... ok
test_item_request_answers_reach_customer (packing.tests_send.TicketReplyAndItemRequestTests.test_item_request_answers_reach_customer) ... ok
test_warehouse_reply_reaches_customer (packing.tests_send.TicketReplyAndItemRequestTests.test_warehouse_reply_reaches_customer) ... ok
test_customer_cannot_open_warehouse_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_customer_cannot_open_warehouse_workspace) ... Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\utils\deprecation.py", line 119, in __call__
    response = self.process_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\middleware\common.py", line 48, in process_request
    host = request.get_host()
           ^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\http\request.py", line 203, in get_host
    raise DisallowedHost(msg)
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
FAIL
test_customer_login_works_in_customer_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_customer_login_works_in_customer_workspace) ... Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\utils\deprecation.py", line 119, in __call__
    response = self.process_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\middleware\common.py", line 48, in process_request
    host = request.get_host()
           ^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\http\request.py", line 203, in get_host
    raise DisallowedHost(msg)
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
FAIL
test_warehouse_cannot_open_customer_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_warehouse_cannot_open_customer_workspace) ... Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\utils\deprecation.py", line 119, in __call__
    response = self.process_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\middleware\common.py", line 48, in process_request
    host = request.get_host()
           ^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\http\request.py", line 203, in get_host
    raise DisallowedHost(msg)
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
FAIL
test_warehouse_login_works_in_warehouse_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_warehouse_login_works_in_warehouse_workspace) ... Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\utils\deprecation.py", line 119, in __call__
    response = self.process_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\middleware\common.py", line 48, in process_request
    host = request.get_host()
           ^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\venv\Lib\site-packages\django\http\request.py", line 203, in get_host
    raise DisallowedHost(msg)
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
FAIL
test_cheapest_wins_not_smallest (packing.tests.RecommendLogicTests.test_cheapest_wins_not_smallest) ... ok
test_empty_order (packing.tests.RecommendLogicTests.test_empty_order) ... ok
test_exact_fit_is_accepted (packing.tests.RecommendLogicTests.test_exact_fit_is_accepted) ... ok
test_fill_percent_reported (packing.tests.RecommendLogicTests.test_fill_percent_reported) ... ok
test_fragile_not_packed_with_heavy (packing.tests.RecommendLogicTests.test_fragile_not_packed_with_heavy) ... ok
test_fragile_with_light_items_is_fine (packing.tests.RecommendLogicTests.test_fragile_with_light_items_is_fine) ... ok
test_item_bigger_than_every_box (packing.tests.RecommendLogicTests.test_item_bigger_than_every_box) ... ok
test_many_small_items_pack_together (packing.tests.RecommendLogicTests.test_many_small_items_pack_together) ... ok
test_no_boxes_configured (packing.tests.RecommendLogicTests.test_no_boxes_configured) ... ok
test_overweight_goes_to_bigger_box (packing.tests.RecommendLogicTests.test_overweight_goes_to_bigger_box) ... ok
test_real_life_ravi_order_gets_medium (packing.tests.RecommendLogicTests.test_real_life_ravi_order_gets_medium) ... ok
test_rotation_is_allowed (packing.tests.RecommendLogicTests.test_rotation_is_allowed) ... ok
test_split_can_be_turned_off (packing.tests.RecommendLogicTests.test_split_can_be_turned_off) ... ok
test_split_message_names_the_fragile_rule (packing.tests.RecommendLogicTests.test_split_message_names_the_fragile_rule) ... ok
test_tie_on_cost_prefers_smaller_volume (packing.tests.RecommendLogicTests.test_tie_on_cost_prefers_smaller_volume) ... ok
test_tiny_item_gets_smallest_box (packing.tests.RecommendLogicTests.test_tiny_item_gets_smallest_box) ... ok
test_too_heavy_splits_into_multiple_boxes (packing.tests.RecommendLogicTests.test_too_heavy_splits_into_multiple_boxes) ... ok
test_volume_ok_but_arrangement_impossible (packing.tests.RecommendLogicTests.test_volume_ok_but_arrangement_impossible) ... ok

======================================================================
ERROR: test_no_fit_is_422_when_split_disabled (packing.tests.ApiTests.test_no_fit_is_422_when_split_disabled)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 154, in test_no_fit_is_422_when_split_disabled
    r = self.post([{"product_id": self.p["Dumbbell"], "quantity": 4}], allow_split=False)
                                  ~~~~~~^^^^^^^^^^^^
KeyError: 'Dumbbell'

======================================================================
ERROR: test_request_is_saved_in_history (packing.tests.ApiTests.test_request_is_saved_in_history)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 132, in test_request_is_saved_in_history
    self.post([{"product_id": self.p["Phone case"], "quantity": 1}])
                              ~~~~~~^^^^^^^^^^^^^^
KeyError: 'Phone case'

======================================================================
ERROR: test_cannot_pack_before_accept_or_accept_twice (packing.tests.CustomerWarehouseFlowTests.test_cannot_pack_before_accept_or_accept_twice)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 238, in test_cannot_pack_before_accept_or_accept_twice
    oid = self.place([("Pen", 1)]).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in place
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in <listcomp>
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                                     ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_customer_places_order (packing.tests.CustomerWarehouseFlowTests.test_customer_places_order)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 199, in test_customer_places_order
    r = self.place([("Pen", 2), ("Chocolate bar", 3)])
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in place
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in <listcomp>
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                                     ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_full_flow_with_recommended_box (packing.tests.CustomerWarehouseFlowTests.test_full_flow_with_recommended_box)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 212, in test_full_flow_with_recommended_box
    oid = self.place([("Pen", 1), ("Pencil box", 1), ("Chocolate bar", 2)]).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in place
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in <listcomp>
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                                     ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_packer_picks_bigger_box_costs_extra (packing.tests.CustomerWarehouseFlowTests.test_packer_picks_bigger_box_costs_extra)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 222, in test_packer_picks_bigger_box_costs_extra
    oid = self.place([("Pen", 1)]).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in place
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in <listcomp>
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                                     ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_warehouse_sees_new_orders_and_customer_sees_own (packing.tests.CustomerWarehouseFlowTests.test_warehouse_sees_new_orders_and_customer_sees_own)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 205, in test_warehouse_sees_new_orders_and_customer_sees_own
    oid = self.place([("Pen", 1)]).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in place
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 185, in <listcomp>
    {"customer_name": name, "items": [{"product_id": self.p[n], "quantity": q} for n, q in items]}),
                                                     ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_cannot_pack_until_everything_is_picked (packing.tests.PickingStepTests.test_cannot_pack_until_everything_is_picked)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 481, in test_cannot_pack_until_everything_is_picked
    oid, ids = self.accepted_order([("Pen", 3), ("Pencil box", 1)])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 469, in accepted_order
    o = self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 470, in <listcomp>
    {"product_id": self.p[n], "quantity": q} for n, q in items]}).json()
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_cannot_pick_before_accept (packing.tests.PickingStepTests.test_cannot_pick_before_accept)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 504, in test_cannot_pick_before_accept
    {"product_id": self.p["Pen"], "quantity": 1}]}).json()
                   ~~~~~~^^^^^^^
KeyError: 'Pen'

======================================================================
ERROR: test_partly_picked_is_still_blocked (packing.tests.PickingStepTests.test_partly_picked_is_still_blocked)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 490, in test_partly_picked_is_still_blocked
    oid, ids = self.accepted_order([("Pen", 3)])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 469, in accepted_order
    o = self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 470, in <listcomp>
    {"product_id": self.p[n], "quantity": q} for n, q in items]}).json()
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_pick_limits (packing.tests.PickingStepTests.test_pick_limits)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 496, in test_pick_limits
    oid, ids = self.accepted_order([("Pen", 3)])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 469, in accepted_order
    o = self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 470, in <listcomp>
    {"product_id": self.p[n], "quantity": q} for n, q in items]}).json()
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_unavailable_item_does_not_need_picking (packing.tests.PickingStepTests.test_unavailable_item_does_not_need_picking)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 508, in test_unavailable_item_does_not_need_picking
    oid, ids = self.accepted_order([("Pen", 1), ("Dumbbell", 1)])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 469, in accepted_order
    o = self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 470, in <listcomp>
    {"product_id": self.p[n], "quantity": q} for n, q in items]}).json()
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_add_items_before_accept_merges_quantity (packing.tests.StockAndAddItemsTests.test_add_items_before_accept_merges_quantity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 281, in test_add_items_before_accept_merges_quantity
    oid = self.order("Pen", 1).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 259, in order
    return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})
                                                                                               ~~~~~~^^^^^^
KeyError: 'Pen'

======================================================================
ERROR: test_add_items_respects_stock (packing.tests.StockAndAddItemsTests.test_add_items_respects_stock)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 296, in test_add_items_respects_stock
    oid = self.order("Pen", 1).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 259, in order
    return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})
                                                                                               ~~~~~~^^^^^^
KeyError: 'Pen'

======================================================================
ERROR: test_cannot_add_items_after_accept (packing.tests.StockAndAddItemsTests.test_cannot_add_items_after_accept)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 290, in test_cannot_add_items_after_accept
    oid = self.order("Pen", 1).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 259, in order
    return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})
                                                                                               ~~~~~~^^^^^^
KeyError: 'Pen'

======================================================================
ERROR: test_cannot_order_more_than_stock (packing.tests.StockAndAddItemsTests.test_cannot_order_more_than_stock)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 275, in test_cannot_order_more_than_stock
    r = self.order("Dumbbell", 7)
        ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 259, in order
    return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})
                                                                                               ~~~~~~^^^^^^
KeyError: 'Dumbbell'

======================================================================
ERROR: test_ordering_reduces_stock (packing.tests.StockAndAddItemsTests.test_ordering_reduces_stock)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 265, in test_ordering_reduces_stock
    self.order("Pen", 3)
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 259, in order
    return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})
                                                                                               ~~~~~~^^^^^^
KeyError: 'Pen'

======================================================================
ERROR: test_out_of_stock_item_cannot_be_ordered (packing.tests.StockAndAddItemsTests.test_out_of_stock_item_cannot_be_ordered)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 269, in test_out_of_stock_item_cannot_be_ordered
    r = self.order("Study table", 1)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 259, in order
    return self.post("/api/orders/place/", {"customer_name": "Aarav", "items": [{"product_id": self.p[name], "quantity": q}]})
                                                                                               ~~~~~~^^^^^^
KeyError: 'Study table'

======================================================================
ERROR: test_restock_and_never_below_zero (packing.tests.StockAndAddItemsTests.test_restock_and_never_below_zero)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 315, in test_restock_and_never_below_zero
    pid = self.p["Study table"]
          ~~~~~~^^^^^^^^^^^^^^^
KeyError: 'Study table'

======================================================================
ERROR: test_cancel_returns_stock_only_before_accept (packing.tests.StockAndInventoryTests.test_cancel_returns_stock_only_before_accept)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 347, in test_cancel_returns_stock_only_before_accept
    oid = self.place([("Pen", 5)]).json()["id"]
          ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 329, in place
    return self.post("/api/orders/place/", {"customer_name": name, "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 330, in <listcomp>
    {"product_id": self.p[n].id, "quantity": q} for n, q in items]})
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_item_unavailable_is_removed_from_packing (packing.tests.StockAndInventoryTests.test_item_unavailable_is_removed_from_packing)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 355, in test_item_unavailable_is_removed_from_packing
    o = self.place([("Pen", 1), ("Dumbbell", 1)]).json()
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 329, in place
    return self.post("/api/orders/place/", {"customer_name": name, "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 330, in <listcomp>
    {"product_id": self.p[n].id, "quantity": q} for n, q in items]})
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_more_than_stock_is_refused_and_ordering_reduces_stock (packing.tests.StockAndInventoryTests.test_more_than_stock_is_refused_and_ordering_reduces_stock)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 342, in test_more_than_stock_is_refused_and_ordering_reduces_stock
    self.assertEqual(self.place([("Pen", 26)]).status_code, 409)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 329, in place
    return self.post("/api/orders/place/", {"customer_name": name, "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 330, in <listcomp>
    {"product_id": self.p[n].id, "quantity": q} for n, q in items]})
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_order_cancelled_when_every_item_unavailable (packing.tests.StockAndInventoryTests.test_order_cancelled_when_every_item_unavailable)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 366, in test_order_cancelled_when_every_item_unavailable
    o = self.place([("Pen", 1)]).json()
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 329, in place
    return self.post("/api/orders/place/", {"customer_name": name, "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 330, in <listcomp>
    {"product_id": self.p[n].id, "quantity": q} for n, q in items]})
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
ERROR: test_out_of_stock_item_cannot_be_ordered (packing.tests.StockAndInventoryTests.test_out_of_stock_item_cannot_be_ordered)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 336, in test_out_of_stock_item_cannot_be_ordered
    r = self.place([("Study table", 1)])
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 329, in place
    return self.post("/api/orders/place/", {"customer_name": name, "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 330, in <listcomp>
    {"product_id": self.p[n].id, "quantity": q} for n, q in items]})
                   ~~~~~~^^^
KeyError: 'Study table'

======================================================================
ERROR: test_warehouse_adds_product_and_restocks (packing.tests.StockAndInventoryTests.test_warehouse_adds_product_and_restocks)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 374, in test_warehouse_adds_product_and_restocks
    self.assertEqual(self.place([("Pen", 1)]).status_code, 201)
                     ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 329, in place
    return self.post("/api/orders/place/", {"customer_name": name, "items": [
                                                                            ^
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 330, in <listcomp>
    {"product_id": self.p[n].id, "quantity": q} for n, q in items]})
                   ~~~~~~^^^
KeyError: 'Pen'

======================================================================
FAIL: test_seed_is_repeatable (packing.tests.ApiTests.test_seed_is_repeatable)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 169, in test_seed_is_repeatable
    self.assertEqual(Product.objects.count(), 10)
AssertionError: 12 != 10

======================================================================
FAIL: test_request_validation_and_duplicates (packing.tests.ProductRequestTests.test_request_validation_and_duplicates)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 410, in test_request_validation_and_duplicates
    self.assertEqual(self.ask(name="pen").status_code, 409)          # already in shop
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 201 != 409

======================================================================
FAIL: test_add_product_validation (packing.tests.StockAndAddItemsTests.test_add_product_validation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests.py", line 312, in test_add_product_validation
    self.assertEqual(self.post("/api/products/add/", {"name": "pen", "length": 1, "width": 1, "height": 1, "weight": 1}).status_code, 409)
AssertionError: 201 != 409

======================================================================
FAIL: test_customer_cannot_open_warehouse_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_customer_cannot_open_warehouse_workspace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests_send.py", line 71, in test_customer_cannot_open_warehouse_workspace
    self.assertEqual(r.status_code, 403)
AssertionError: 400 != 403

======================================================================
FAIL: test_customer_login_works_in_customer_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_customer_login_works_in_customer_workspace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests_send.py", line 79, in test_customer_login_works_in_customer_workspace
    self.assertEqual(r.status_code, 200)
AssertionError: 400 != 200

======================================================================
FAIL: test_warehouse_cannot_open_customer_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_warehouse_cannot_open_customer_workspace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests_send.py", line 75, in test_warehouse_cannot_open_customer_workspace
    self.assertEqual(r.status_code, 403)
AssertionError: 400 != 403

======================================================================
FAIL: test_warehouse_login_works_in_warehouse_workspace (packing.tests_send.WorkspaceRoleLoginTests.test_warehouse_login_works_in_warehouse_workspace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\vaish\Downloads\Box_Selection\QuickPack\packing\tests_send.py", line 83, in test_warehouse_login_works_in_warehouse_workspace
    self.assertEqual(r.status_code, 200)
AssertionError: 400 != 200

----------------------------------------------------------------------
Ran 88 tests in 66.166s

FAILED (failures=7, errors=25)
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...