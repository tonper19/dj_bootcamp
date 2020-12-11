"""dj_bootcamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from products.views import (
    search_view,
    product_detail_view,
    product_create_view,
    product_api_detail_view,
    product_list_view,
    # bad_view,
)
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)
from orders.views import (
    order_checkout_view,
)
# awod
from homepage.views import HomepageView

urlpatterns = [
    path('admin/', admin.site.urls),
    # own
    path("login/", login_view),
    path("logout/", logout_view),
    path("register/", register_view),

    path("search/", search_view),
    path("products/create/", product_create_view),
    path("products/<int:pk>/", product_detail_view),  # dynamic url
    path("api/products/<int:pk>/", product_api_detail_view),  # dynamic url
    path("products/", product_list_view),  # dynamic url

    path("checkout/", order_checkout_view),  # dynamic url

    # path("bad-view-dont-use/", bad_view),
    # awod
    path("", HomepageView.as_view(), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
