from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import OrderProductForm
from .models import Order
from .serializers import OrderCreateSerializer


class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()


class CreateOrderProductView(LoginRequiredMixin, CreateView):
    template_name = "orders/create_order_product.html"
    form_class = OrderProductForm
    success_url = reverse_lazy("my_order")

    def form_valid(self, form):
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )
        form.instance.order = order
        form.instance.quantity = 1
        form.save()
        return super().form_valid(form)


class OrderCreateAPI(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    "id": order.id,
                    "user": order.user.id,
                    "total": str(order.total),
                    "items": [
                        {
                            "product": item.product.name,
                            "quantity": item.quantity,
                            "subtotal": str(item.subtotal),
                        }
                        for item in order.orderproduct_set.all()
                    ],
                },
                status=201,
            )
        return Response(serializer.errors, status=400)
