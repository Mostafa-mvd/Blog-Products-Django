from django.urls import path
from . import views


app_name = "store"

urlpatterns = [
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("finalized-order/", views.finalized_order, name="finalized_order"),
    path("view-cart/", views.view_cart, name="view_cart"),
    path("delete-from-cart/<int:product_id>/", views.delete_table_row, name="delete_from_cart"),
    path("decrease_product_number/", views.decrease_product_from_cart, name="decrease_product_number"),
    path("show-finalized-order/", views.ListOrdersView.as_view(), name="show_finalized_order"),
    path("get-receipt/<int:pk>/", views.PrintOrderView.as_view(), name='receipt'),
]
