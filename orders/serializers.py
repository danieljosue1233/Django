from rest_framework import serializers

from orders.models import Order, OrderProduct
from products.models import Product


class OrderProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    items = OrderProductSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Debe incluir al menos un producto.")
        return items

    def validate(self, data):
        for item in data["items"]:
            if not Product.objects.filter(id=item["product_id"]).exists():
                raise serializers.ValidationError(
                    {"product_id": f"Producto con id {item['product_id']} no existe."}
                )
        return data

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user_id = validated_data.get("user_id")

        if user_id:
            from django.contrib.auth.models import User

            user = User.objects.get(id=user_id)
        else:
            user = self.context["request"].user

        order = Order.objects.create(user=user, is_active=True)
        for item in items_data:
            product = Product.objects.get(id=item["product_id"])
            OrderProduct.objects.create(
                order=order, product=product, quantity=item["quantity"]
            )
        return order
