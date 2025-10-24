from django.db import models
from django.conf import settings

class Ride(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('assigned', 'Assigned'),
        ('dropped', 'Dropped'),
        ('cancelled', 'Cancelled'),
    )

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rides_as_rider',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rides_as_customer',
        on_delete=models.CASCADE
    )
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    total_distance = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.customer.username} → {self.destination}"

    # ✅ Helper to create a ride event
    def add_event(self, description):
        last = self.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        RideEvent.objects.create(ride=self, step_count=next_step, description=description)


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, related_name='events', on_delete=models.CASCADE)
    step_count = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('step_count',)

    def __str__(self):
        return f"Step {self.step_count}: {self.description}"