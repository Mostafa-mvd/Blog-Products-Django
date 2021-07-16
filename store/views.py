import logging

import weasyprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
import inventory.models
from inventory import models, views
from rest_framework import status, viewsets
from store import models as store_models
from store import serializers
from store import permissions as store_permissions
from store.permissions import IsCustomerOrReadOnly
from store.models import OrderItem, Order
from rest_framework.exceptions import NotAuthenticated
from rest_framework import permissions as rest_presmissions
from rest_framework.decorators import action
# from rest_framework import permissions


logger = logging.getLogger(__name__)

def add_to_cart(request, product_id):
    product_instance = get_object_or_404(models.Product, pk=product_id)

    if not product_instance.can_be_sold():
        messages.error(request, "امکان فروش ندارد.")
        return redirect("inventories:product_lst")

    if not product_instance.is_qty_in_stuck(1):
        messages.error(request, "این محصول به تعداد مورد نظر موجود نیست.")
        return redirect("inventories:product_lst")

    # if 'cart' not in request.session.keys():
    #    def_dict = defaultdict(int)
    #    request.session["cart"] = def_dict

    cart = request.session.get("cart", defaultdict(int))

    # Method A:
    #    request.session['cart'] += [
    #        {
    #            'product_id': product_instance.pk,
    #            'qty': 1
    #        }
    #    ]

    # Method B-1:
    # if str(product_instance.pk) in request.session['cart'].keys():
    #    request.session['cart'][str(product_instance.pk)] += 1
    # else:
    #    request.session['cart'][str(product_instance.pk)] = 1

#    Method B-2:
#    try:
#        request.session['cart'][product_instance.pk] += 1
#    except KeyError:
#        request.session['cart'][product_instance] = 1

    # Method C:
    # request.session['cart'][str(product_instance.pk)] += 1

    # Method D:
    cart[str(product_instance.pk)] += 1
    request.session["cart"] = cart

    logger.info(f"Order added to cart #{product_id}")

    # del request.session['cart']
    # request.session.modified = True
    request.session.save()

    # print(request.session['cart'])
    messages.success(request, "کالای شما به سبد افزوده شد.")
    return redirect("inventories:product_lst")


def view_cart(request):
    object_list = []

    for item in request.session.get('cart', []):
        object_list += [
            {
                'product': inventory.models.Product.objects.get(pk=int(item)),
                'qty': request.session["cart"][item]
            }
        ]

    return render(
        request,
        "store/view_cart.html",
        context={
            "object_list": object_list
        }
    )


def delete_table_row(request, product_id):
    """
    Delete product row in the basket table
    """

    request.session['cart'].pop(str(product_id), None)
    # request.session.save()
    request.session.modified = True
    messages.success(request, 'deleted')
    return redirect("store:view_cart")


@require_POST
@csrf_exempt
def decrease_product_from_cart(request):
    """
    Decrease number of product in cart
    """

    product_id = request.POST.get("product_id", None)
    product_id = str(product_id)

    if product_id:
        try:
            request.session['cart'][product_id] -= 1
            request.session.save()
            return JsonResponse(
                {
                    'success': True,
                    'qty': request.session['cart'][product_id]
                },
                status=200
            )
        except KeyError:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Invalid data.\nNot in the cart'
                },
                status=400
            )
    else:
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid data.'
            },
            status=400
        )


"""
REST API View
"""


class OrderViewSet(viewsets.ModelViewSet):
    queryset = store_models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    # permission_classes = [store_permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsCustomerOrReadOnly]

    #filter with your queryset class attr

    # def filter_queryset(self, queryset):
    #    super().filter_queryset(queryset)
    #    return queryset.filter(customer=self.request.user)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            raise NotAuthenticated("You are not authenticated")
        # return qs.filter(customer=self.request.user)
        return qs.filter_by_customer(self.request.user)


    @action(detail=True, description="Cancel An Order")
    def cancel_order(self, request, *args, **kwargs):
        order_instance = self.get_object()
        order_instance.set_as_canceled()
        order_serializer = self.get_serializer(instance=order_instance)
        return JsonResponse(order_serializer.data, status=status.HTTP_202_ACCEPTED)


@login_required
def finalized_order(request):
    cart = request.session.get("cart", None)

    if not cart:
        messages.error(request, "سبد شما خالی است.")
        return redirect("inventories:product_lst")

    order_instance = Order.objects.create(customer=request.user)

    for product_id in cart:
        product = models.Product.objects.get(pk=product_id)
        qty = cart[product_id]

        if not product.is_qty_in_stuck(qty):
            messages.error(request, "انبار موجودی کافی ندارد")
            return redirect("store:view_cart")

        order_item_instance = OrderItem.objects.create(
            order=order_instance,
            qty=qty,
            product=product,
            price=product.price
        )

        product.deduct_from_stock(qty)

    messages.info(request, 'سفارش با موفقیت ثبت شد.')
    request.session.pop('cart')
    # del request.session["cart"]
    request.session.modified = True
    return redirect('inventories:product_lst')


class ListOrdersView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 6

    def get_queryset(self):
        qs = super(ListOrdersView, self).get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs


class PrintOrderView(LoginRequiredMixin, DetailView):
    model = Order

    def get(self, request, *args, **kwargs):
        get_response = super().get(request, args, kwargs)
        content = get_response.rendered_content
        receipt_pdf = weasyprint.HTML(string=content).write_pdf()
        response = HttpResponse(receipt_pdf, content_type='application/pdf')
        return response


class OrderItemsViewSets(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemsSerializer
    permission_classes = [rest_presmissions.IsAuthenticated, store_permissions.IsCustomerOrReadOnlyForOrderItems]

