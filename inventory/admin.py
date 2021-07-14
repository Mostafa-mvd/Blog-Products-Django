from django.contrib import admin
from . import models


admin.site.site_header = "فروشگاه هنری"


@admin.action(description="Active product")
def set_product_as_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Inactive product")
def set_product_as_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'qty_in_stock',
        'is_active',
        'type',
        'price',
        'quality',
    )

    list_display_links = (
        'pk',
        'name',
    )

    list_editable = (
        'price',
        'qty_in_stock',
    )

    search_fields = (
        'name__icontains',
        'description__icontains',
    )

    list_filter = (
        'is_active',
        'type',
    )

    actions = (
        set_product_as_active,
        set_product_as_inactive,
    )

    ordering = ("name", "-is_active", "-qty_in_stock", "-pk")

    list_per_page = 3
