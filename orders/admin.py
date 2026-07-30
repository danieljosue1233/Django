from django.contrib import admin

from .models import Order, OrderProduct


class OrderProductInlineAdmin(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inlines = [OrderProductInlineAdmin]


admin.site.register(Order, OrderAdmin)
