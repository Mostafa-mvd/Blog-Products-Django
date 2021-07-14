from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from store.signals import order_placed
from users.models import Profile


@receiver(order_placed)
def send_email_when_order_is_placed(sender, **kwargs):
    """
    A call back for sending email when order is placed.
    """

    print("hello world")

    # split_import = str(sender).split(".")
    # order = "Order\'>"

    # if order == split_import[2]:
    #    print("hello world")


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, **kwargs):
    # if created:
    #       Profile.objects.create(user=instance).save()

    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"]).save()
