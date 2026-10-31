"""Separate login sessions for the customer and warehouse dashboards.

Normally Django keeps ONE login cookie per browser, so signing in to the warehouse
dashboard would sign the customer out (and the other way round).  This middleware gives
the warehouse dashboard its own cookie (`sessionid_warehouse`), so both dashboards can be
open and logged in at the same time in one browser, each with its own account.

A request counts as "warehouse" when its path starts with /warehouse or it carries the
header `X-Workspace: warehouse` (the warehouse page adds this header to its API calls).
It must sit BEFORE SessionMiddleware in settings.MIDDLEWARE.
"""

DEFAULT_COOKIE = "sessionid"
WAREHOUSE_COOKIE = "sessionid_warehouse"


class WorkspaceSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def _is_warehouse(request):
        if str(request.headers.get("X-Workspace", "")).lower() == "warehouse":
            return True
        return request.path.startswith("/warehouse")

    def __call__(self, request):
        warehouse = self._is_warehouse(request)
        if warehouse:
            # Never let the customer's login leak into the warehouse dashboard.
            request.COOKIES.pop(DEFAULT_COOKIE, None)
            own = request.COOKIES.get(WAREHOUSE_COOKIE)
            if own:
                request.COOKIES[DEFAULT_COOKIE] = own
        response = self.get_response(request)
        if warehouse and DEFAULT_COOKIE in response.cookies:
            morsel = response.cookies.pop(DEFAULT_COOKIE)
            response.cookies[WAREHOUSE_COOKIE] = morsel.value
            for key, val in morsel.items():
                if val != "":
                    response.cookies[WAREHOUSE_COOKIE][key] = val
        return response
