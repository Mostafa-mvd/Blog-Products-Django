from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels
from store import enums
from store.signals import order_placed
import logging


logger = logging.getLogger(__name__)


# chain objects manager
# class OrderObjectManager(models.manager):

#     def filter_by_customer(self, customer):
#         return self.filter(customer=customer)


# chain queryset like objects
class OrderQuerySetManager(models.QuerySet):
    
    def filter_by_customer(self, customer):
        return self.filter(customer=customer)


class Order(models.Model):
    # get_user_model() Returns the User model that is active in this project.
    # It is useful when we modified the django user model or created new user model

    customer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_("Creator"))
    created_on = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_("DataTime"))
    status = models.CharField(
        verbose_name=_("Status"),
        help_text="وضعیت سفارش",
        choices=enums.OrderStatus.choices,
        default=enums.OrderStatus.CREATED,
        max_length=100
    )

    # main_objects = models.Manager()
    objects = OrderQuerySetManager.as_manager()

    def __str__(self):
        return f'Order #{self.pk} for {self.customer.get_full_name()}'

    def get_formatted_time(self):
        return self.created_on.strftime("%Y-%m-%d, %H:%M:%S")

    @cached_property
    def formatted_date(self):
        return self.get_formatted_time()

    def set_as_canceled(self):
        self.status = enums.OrderStatus.CANCELED
        self.save()

        logger.info(f"Order #{self.pk} was set as CANCELED.")

    def save(self, **kwargs):
        # Is this object new or edited
        if self.pk is True:
            created = True
        else:
            created = False

        super(Order, self).save(**kwargs)

        order_placed.send(
            sender=self.__class__,
            instance=self,
            created=created,
            msg="Hi there"
        )

        logger.debug(f"order_placed signal was sent for Order #{self.pk}")

    def get_total_qty(self):
        # s = 0
        # for item in self.orderitem_set.all():
        #     s += item.qty
        # return s

        return self.orderitem_set.aggregate(Sum('qty')).get("qty__sum", 0)

    def get_grand_total(self):
        # s = 0
        # for item in self.orderitem_set.all():
        #    s += (item.price * item.qty)
        # return s

        # F method is for fields
        return self.orderitem_set.all().annotate(grand_total=F("qty") * F("price")) \
            .aggregate(Sum('grand_total'))['grand_total__sum']


class OrderItem(models.Model):
    order = models.ForeignKey("store.Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, verbose_name=_("Product"))
    qty = models.PositiveIntegerField(default=1, verbose_name=_("QtyInStock"))
    discount = models.FloatField(default=0, verbose_name=_("Discount"))
    price = models.PositiveIntegerField(verbose_name=_("Price"))

    def get_total(self):
        return self.qty * self.price
