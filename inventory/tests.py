from django.test import TestCase
from .models import Product


class ProductTestCase(TestCase):

    def setUp(self):
        from .enums import ProductTypes
        Product.objects.create(
            name="عکس لباس",
            description="لباس می باشد",
            qty_in_stock=20,
            is_active=True,
            type=ProductTypes.PRINT
        )

    def test_deduct_from_stock(self):
        obj = Product.objects.first()
        qty = obj.deduct_from_stock(10)
        self.assertEqual(qty, 10)
