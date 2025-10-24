from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, SignInForm
from rides.models import Ride
from django.db import models



def index(request):
    return render(request, 'dashboard/index.html')

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'accounts/signup.html', {'form': form})


class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'accounts/signin.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('/')
        return render(request, 'accounts/signin.html', {'form': form, 'invalid': True})


@login_required
def profile_view(request):
    user = request.user

    if user.user_role == 'rider':
        # all completed (dropped) rides for that rider
        completed = Ride.objects.filter(rider=user, status='dropped').order_by('-updated_at')
        # total distance overall
        total_distance = completed.aggregate(total=models.Sum('total_distance'))['total'] or 0

        # optional date filter (yyyy-mm-dd)
        date_str = request.GET.get('date')
        date_total = None
        rides_by_date = completed
        if date_str:
            try:
                from datetime import datetime
                d = datetime.fromisoformat(date_str).date()
                rides_by_date = completed.filter(updated_at__date=d)
                date_total = rides_by_date.aggregate(total=models.Sum('total_distance'))['total'] or 0
            except Exception:
                date_total = None

        return render(request, 'accounts/profile_rider.html', {
            'total_distance': total_distance,
            'rides': rides_by_date,
            'date_total': date_total,
        })

    else:
        # customer profile
        rides = Ride.objects.filter(customer=user).order_by('-created_at')
        return render(request, 'accounts/profile_customer.html', {'rides': rides})

def add_event(self, description):
    last = self.events.order_by('-step_count').first()
    next_step = (last.step_count + 1) if last else 1
    from .models import RideEvent
    RideEvent.objects.create(ride=self, step_count=next_step, description=description)

def signout_view(request):
    logout(request)
    return redirect('home')  #


def logout_view(request):
    logout(request)
    return redirect('/')
