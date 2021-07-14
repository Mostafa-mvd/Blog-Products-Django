from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from . import models
from . import serializers


class ListProductView(ListView):
    model = models.Product
    template_name = "inventories/product_list.html"
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().order_by("-name")


"""
REST API View
"""


class ProductList(ListAPIView):
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer


@csrf_exempt
def product_list(request):
    if request.method == "GET":
        qs = models.Product.objects.all()
        serializer = serializers.ProductSerializer(qs, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    elif request.method == "POST":
        # convert or parse json to dict object
        data = JSONParser().parse(request)
        serializer = serializers.ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ProductList2(APIView):

    def get(self, request, format=None):
        qs = models.Product.objects.all()
        serializer = serializers.ProductSerializer(qs, many=True)
        return Response(serializer.data)

# you can use Mixins for your view for reducing your codes.
