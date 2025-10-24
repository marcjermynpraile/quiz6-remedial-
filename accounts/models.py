from django.contrib.auth.models import AbstractUser
from django.db import models
USER_ROLES = (('customer','Customer'),('rider','Rider'),('staff','Staff'),)
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    user_role = models.CharField(max_length=12, choices=USER_ROLES, default='customer')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join([p for p in parts if p])
