from django import forms
from .models import Ride, RideEvent
import random

from django import forms
from .models import Ride

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup_location', 'destination', 'total_distance', 'price']

    def clean(self):
        cleaned = super().clean()
        total_distance = cleaned.get('total_distance')
        price = cleaned.get('price')

        if total_distance and price and price <= 0:
            self.add_error('price', 'Price must be greater than zero.')

        return cleaned


class RideEventForm(forms.ModelForm):
    class Meta:
        model = RideEvent
        fields = ['description']