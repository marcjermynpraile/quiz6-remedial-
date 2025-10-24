from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser
from rides.models import Ride
from decimal import Decimal


def staff_required(view):
    return user_passes_test(lambda u: u.is_authenticated and u.user_role == 'staff')(view)


@login_required
def index(request):
    user = request.user

    # Filter rides depending on user role
    if user.user_role == 'customer':
        rides = Ride.objects.filter(customer=user).order_by('-created_at')
    elif user.user_role == 'rider':
        rides = Ride.objects.filter(rider=user).order_by('-created_at')
    else:
        rides = Ride.objects.all().order_by('-created_at')

    context = {
        'user': user,
        'rides': rides,
    }
    return render(request, 'dashboard/index.html', context)

@staff_required
def dashboard_home(request):
    total_users = CustomUser.objects.count()
    total_rides = Ride.objects.count()
    confirmed_rides = Ride.objects.filter(status='assigned').count()
    cancelled_rides = Ride.objects.filter(status='cancelled').count()
    recent_rides = Ride.objects.order_by('-created_at')[:8]

    context = {
        'total_users': total_users,
        'total_rides': total_rides,
        'confirmed_rides': confirmed_rides,
        'cancelled_rides': cancelled_rides,
        'recent_rides': recent_rides,
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_required
def users_list(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard/users_list.html', {'users': users})


@staff_required
def add_balance(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        amount = Decimal(request.POST.get('amount'))
        user = CustomUser.objects.get(pk=user_id)
        user.balance += amount
        user.save()
        return redirect('dashboard:users')

    users = CustomUser.objects.all()
    return render(request, 'dashboard/add_balance.html', {'users': users})
