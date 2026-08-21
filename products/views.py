from django.urls import reverse_lazy
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView

from products.forms import ProductForm
from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.
class ProductFormView(generic.FormView):
    template_name = "products/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("add_product")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/list_product.html"
    context_object_name = "products"


class ProductListAPI(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreateAPI(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
