# from re import T
from rest_framework import serializers
# from rest_framework.renderers import JSONRenderer
# import csv
from . import models


# Create serializer with Model
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = (
            'name',
            'description',
            'price',
        )


# # Create serializer by yourself
# class FruitSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(
#         required=True, allow_null=False, allow_blank=False, max_length=50)

#     def create(self, validated_data):
#         csv_handler = open("fruit_file.csv", "w")
#         writer = csv.writer(csv_handler)
#         writer.writerow(validated_data)

#         # print(validated_data)
#         return True

#     def update(self, instance, validated_data):
#         pass


# # like data = request.data
# fruit = FruitSerializer(data={'name': 'Apple'})
# fruit.is_valid()
# print(fruit.validated_data)
# fruit.save()  # for calling create() or update method


# content = JSONRenderer().render(fruit.validated_data)
# print(content)
