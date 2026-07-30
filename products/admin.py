from typing import ClassVar

from django.contrib import admin

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    model: ClassVar = Product
    list_display: ClassVar[list[str]] = ["name", "price"]
    search_fields: ClassVar[list[str]] = ["name"]


admin.site.register(Product, ProductAdmin)
