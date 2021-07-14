from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import enums


class Product(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name=_("Name")
    )

    description = models.TextField(
        verbose_name=_("Description")
    )

    qty_in_stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Number")
    )

    # does_exist, is_product_existing
    is_active = models.BooleanField(
        default=False,
        help_text=_("This product will sell?")
    )

    type = models.CharField(
        max_length=100,
        choices=enums.ProductTypes.choices,
        verbose_name=_("Type")
    )

    quality = models.CharField(
        max_length=100,
        choices=enums.ProductQuality.choices,
        blank=True,
        null=True,
        verbose_name=_("Quality")
    )

    price = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name=_("Price")
    )

    product_image = models.ImageField(verbose_name=_("Image"),
                                      upload_to="media/products",
                                      blank=True,
                                      null=True)

    def __str__(self):
        return self.name

    def can_be_sold(self):
        return self.is_active

    def is_qty_in_stuck(self, qty):
        return qty <= self.qty_in_stock

    def deduct_from_stock(self, qty):
        self.qty_in_stock -= qty
        self.save()
        return self.qty_in_stock
