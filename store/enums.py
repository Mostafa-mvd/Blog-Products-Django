from django.db import models
from django.utils.translation import ugettext as _


class OrderStatus(models.TextChoices):
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELED = 'CANCELED', _('Canceled')
    SUSPENDED = 'SUSPENDED', _('Suspended')
    CREATED = 'CREATED', _('Created')
