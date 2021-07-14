import jdatetime
import pytz
from django.core.management import BaseCommand

from mywebsite import settings
from store.enums import OrderStatus
from store.models import Order


class Command(BaseCommand):
    help = "Cancel uncompleted orders."

    def handle(self, *args, **options):
        qs = Order.objects.filter(status=OrderStatus.CREATED)

        for order in qs:
            today = jdatetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
            order_date = order.created_on
            diff = today - order_date

            if diff.days > 1:
                order.set_as_canceled()
                print("canceled order {}".format(order.pk))
            else:
                print("No orders are older than 1 day.")
