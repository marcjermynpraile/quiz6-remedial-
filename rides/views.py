from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import random
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.utils import timezone
from django.db import models
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse






from .models import Ride, RideEvent
from .forms import RideForm, RideEventForm



def index(request):
    return redirect('rides:list')


# ----------------- RIDE VIEWS -----------------
# ===== CREATE RIDE: validate balance but DO NOT deduct until completion =====
class RideListView(LoginRequiredMixin, ListView):
    model = Ride
    template_name = 'rides/ride_list.html'
    context_object_name = 'rides'

    def get_queryset(self):
        user = self.request.user
        if user.user_role == 'customer':
            # show only rides booked by this customer
            return Ride.objects.filter(customer=user).order_by('-created_at')
        elif user.user_role == 'rider':
            # show rides assigned to this rider
            return Ride.objects.filter(rider=user).order_by('-created_at')
        elif user.user_role == 'staff':
            # staff can see all rides
            return Ride.objects.all().order_by('-created_at')
        return Ride.objects.none()

class CreateRide(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideForm
    template_name = 'rides/ride_form.html'
    success_url = reverse_lazy('rides:list')

    def form_valid(self, form):
        # Assign the logged-in user as the customer
        form.instance.customer = self.request.user

        # Auto-generate random distance if not provided
        if not form.instance.total_distance:
            form.instance.total_distance = random.randint(10, 30)

        # Price validation
        price = form.cleaned_data.get('price') or form.instance.price
        if price is None:
            price = round(form.instance.total_distance * 10, 2)
            form.instance.price = price

        if self.request.user.balance < price:
            form.add_error('price', 'Price cannot be greater than your available balance.')
            return self.form_invalid(form)

        # Save the ride
        response = super().form_valid(form)

        # Create initial ride event
        try:
            self.object.add_event('Ride created by customer')
        except Exception:
            pass

        return response



# ✅ Move this OUTSIDE the class above
class RideDetailView(LoginRequiredMixin, DetailView):
    model = Ride
    template_name = 'rides/ride_detail.html'
    context_object_name = 'ride'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.object.events.order_by('step_count')
        return context


class DeleteRide(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    template_name = 'rides/ride_confirm_delete.html'
    success_url = reverse_lazy('rides:list')

    def test_func(self):
        ride = self.get_object()
        user = self.request.user
        return user.user_role == 'staff' or (user == ride.customer and ride.rider is None)

    def delete(self, request, *args, **kwargs):
        ride = self.get_object()
        last = ride.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        ride.events.create(step_count=next_step, description='Ride deleted')
        return super().delete(request, *args, **kwargs)

# ===== RIDER DASHBOARD: show available rides + assigned rides =====
@login_required
def rider_dashboard(request):
    user = request.user
    if user.user_role != 'rider':
        return redirect('rides:list')

    # available rides: status 'created' (not yet assigned)
    available = Ride.objects.filter(status='created').order_by('-created_at')
    # rides assigned to this rider (all statuses)
    my_rides = Ride.objects.filter(rider=user).order_by('-created_at')

    # total distance completed today for this rider
    today = timezone.localdate()
    total_today = (
        my_rides.filter(status='dropped', updated_at__date=today)
        .aggregate(total=models.Sum('total_distance'))['total'] or 0
    )

    return render(request, 'rides/rider_dashboard.html', {
        'available_rides': available,
        'my_rides': my_rides,
        'total_today': total_today,
    })


# ===== Accept a ride (rider clicks Accept) =====
@login_required
@require_POST
def accept_ride(request, pk):
    user = request.user
    if user.user_role != 'rider':
        return HttpResponseForbidden("Only riders can accept rides.")

    # ensure atomic change
    with transaction.atomic():
        ride = get_object_or_404(Ride.objects.select_for_update(), pk=pk)
        # ensure still available
        if ride.status != 'created' or ride.rider is not None:
            return HttpResponseForbidden("Ride is no longer available.")

        ride.rider = user
        ride.status = 'assigned'
        ride.updated_at = timezone.now()
        ride.save()

        # create ride event with step_count increment (e.g. step_count 2)
        last = ride.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        # we want Rider accepted to be step_count 2 per your requirement,
        # but if there is no previous event, next_step will be 1; that's ok.
        ride.events.create(step_count=next_step, description='Rider accepted the ride')

    return HttpResponseRedirect(reverse('rides:rider_dashboard'))


# ===== Rider marks ride complete (drop) =====
@login_required
@require_POST
def complete_ride(request, pk):
    user = request.user
    if user.user_role != 'rider':
        return HttpResponseForbidden("Only riders can complete rides.")

    with transaction.atomic():
        ride = get_object_or_404(Ride.objects.select_for_update(), pk=pk)
        # only the assigned rider can complete
        if ride.rider_id != user.id or ride.status != 'assigned':
            return HttpResponseForbidden("You are not allowed to complete this ride.")

        # mark as dropped/completed
        ride.status = 'dropped'
        ride.updated_at = timezone.now()
        ride.save()

        # create event step increment: "Ride Complete"
        last = ride.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        ride.events.create(step_count=next_step, description='Ride Complete')

        # transfer balances now: deduct customer, credit rider
        price = ride.price or 0
        customer = ride.customer

        # validate customer has enough balance (should have been checked on create)
        if customer.balance < price:
            # you can choose: forbid completion or allow negative; I'll forbid
            raise ValueError("Customer does not have enough balance to pay for the ride.")

        customer.balance -= price
        customer.save()

        user.balance += price
        user.save()

    return HttpResponseRedirect(reverse('rides:rider_dashboard'))


# ===== UpdateRide: only customer if no rider; rider may update status (handled above) =====
class UpdateRide(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    form_class = RideForm
    template_name = 'rides/ride_form.html'
    success_url = reverse_lazy('rides:list')

    def test_func(self):
        ride = self.get_object()
        user = self.request.user
        # staff can always update
        if user.user_role == 'staff':
            return True
        # customer can edit only if no rider assigned
        if user == ride.customer and ride.rider is None:
            return True
        # assigned rider can update limited fields via separate view (we keep UpdateRide restricted)
        return False

    def form_valid(self, form):
        # create a ride_event about the update
        response = super().form_valid(form)
        ride = self.object
        last = ride.events.order_by('-step_count').first()
        next_step = (last.step_count + 1) if last else 1
        ride.events.create(step_count=next_step, description='Ride updated')
        return response



class DeleteRideEvent(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RideEvent
    template_name = 'rides/rideevent_confirm_delete.html'

    def test_func(self):
        return self.request.user.user_role == 'staff'

    def get_success_url(self):
        return reverse_lazy('rides:event_list', kwargs={'ride_id': self.object.ride.id})
