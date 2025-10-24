from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ride, RideEvent
from decimal import Decimal
from django.db import transaction
@receiver(post_save, sender=Ride)
def create_on_create(sender, instance, created, **kwargs):
    if created:
        RideEvent.objects.create(ride=instance, step_count=1, description='User created a ride.')
@receiver(pre_save, sender=Ride)
def handle_status_changes(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = Ride.objects.get(pk=instance.pk)
    if old.rider is None and instance.rider is not None:
        last = instance.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        RideEvent.objects.create(ride=instance, step_count=next_step, description='Rider accepted the ride.')
        instance.status = 'assigned'
    if old.status != 'dropped' and instance.status == 'dropped':
        last = instance.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        RideEvent.objects.create(ride=instance, step_count=next_step, description='Ride Complete')
        customer = instance.customer
        rider = instance.rider
        if customer.balance < instance.price:
            raise ValueError('Customer does not have enough balance to pay.')
        with transaction.atomic():
            customer.balance -= instance.price
            rider.balance += instance.price
            customer.save()
            rider.save()
