"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
import debug_toolbar

from users import views as users_views
from store import views as store_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"show-users", users_views.UserViewSet)
router.register(r"show-orders", store_views.OrderViewSet)
router.register(r"show-orderitems", store_views.OrderItemsViewSets)


urlpatterns = [
    path("blog/", include("blog.urls", namespace="blog")),
    path("inventories/", include("inventory.urls", namespace="inventories")),
    path("users/", include("users.urls", namespace="users")),
    path("store/", include("store.urls", namespace="store")),
    path('admin/logout/', lambda request: redirect('users:logout_user', permanent=False)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
