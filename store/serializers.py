from rest_framework import fields
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from . import models
from users import serializers as users_serializers


class OrderSerializer(HyperlinkedModelSerializer):

    # customer = users_serializers.UsersSerializer()

    class Meta:
        model = models.Order
        fields = (
            'pk',
            'customer',
            'status',
            'orderitem_set'
        )


class OrderItemsSerializer(ModelSerializer):

    class Meta:
        model = models.OrderItem

        fields = [
            'pk',
            'product',
            'qty',
            'discount',
            'price',
        ]

        read_only_fields = [
            'pk',
        ]
