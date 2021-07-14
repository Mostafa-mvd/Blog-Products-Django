from django.urls import path
from . import views

app_name = "inventories"

urlpatterns = [
    path(
        "product_list/",
        views.ListProductView.as_view(),
        name="product_lst"
    ),

    path(
        "api/v1/",
        views.ProductList.as_view(),
        name="api_product"
    ),

    path(
        "api/product_list",
        views.product_list,
        name="api_product_list"
    ),

    path(
        "api/my_product_list",
        views.ProductList2.as_view(),
        name="my_product_api"
    ),
]
