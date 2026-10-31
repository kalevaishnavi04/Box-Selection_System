"""
URL configuration for boxsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path

from packing.views import index, customer_workspace, warehouse_workspace, login_page, signup_page, warehouse_login_page, warehouse_signup_page, logout_page
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from packing.views import index, customer_workspace, warehouse_workspace, login_page, signup_page, warehouse_login_page, warehouse_signup_page, logout_page

urlpatterns = [
    # Open the upgraded customer application at the site root.
    path('', customer_workspace, name='home'),
    # Keep the original box recommendation and packing interface available.
    path('packing/', index, name='packing-home'),
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login-page'),
    path('signup/', signup_page, name='signup-page'),
    path('warehouse/login/', warehouse_login_page, name='warehouse-login-page'),
    path('warehouse/signup/', warehouse_signup_page, name='warehouse-signup-page'),
    path('logout/', logout_page, name='logout-page'),
    path('customer/', customer_workspace, name='customer-workspace'),
    path('warehouse/', warehouse_workspace, name='warehouse-workspace'),
    path('api/', include('packing.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
