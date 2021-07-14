from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = (
        "order",
        "product",
        'qty',
        'price',
        'discount',
    )


@admin.register(models.Order)
class StoreAdmin(admin.ModelAdmin):
    inlines = (
        OrderItemInline,
    )

    list_display = (
        'pk',
        'customer',
        'created_on',
        'status',
    )

    ordering = ("created_on", "-customer", "pk")

    list_editable = ("status",)

    list_filter = (
        ('created_on', DateRangeFilter),
        'status',
        'created_on',
        'customer',
    )

    search_fields = (
        'pk',
        'status__iexact',
        'customer__username__icontains',
        'customer__username__exact',
    )

    list_per_page = 3
