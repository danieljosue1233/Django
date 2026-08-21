from django.urls import path

from .views import CreateOrderProductView, MyOrderView, OrderCreateAPI

urlpatterns = [
    path("my-order/", MyOrderView.as_view(), name="my_order"),
    path("add-product/", CreateOrderProductView.as_view(), name="add_product"),
    path("api/create/", OrderCreateAPI.as_view(), name="order_create_api"),
]
