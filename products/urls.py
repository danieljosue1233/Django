from django.urls import path

from products.views import (
    ProductCreateAPI,
    ProductFormView,
    ProductListAPI,
    ProductListView,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="list_product"),
    path("api/", ProductListAPI.as_view(), name="product_list_api"),
    path("api/create/", ProductCreateAPI.as_view(), name="product_create_api"),
    path("add/", ProductFormView.as_view(), name="add_product"),
]
