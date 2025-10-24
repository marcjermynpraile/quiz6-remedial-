from django.urls import path
from . import views
from .views import (
    CreateRide, RideListView, RideDetailView,
    UpdateRide, DeleteRide

)
app_name = 'rides'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.RideListView.as_view(), name='list'),
    path('create/', views.CreateRide.as_view(), name='create'),
    path('<int:pk>/', views.RideDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdateRide.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteRide.as_view(), name='delete'),
    path('book/', views.CreateRide.as_view(), name='book'),
    path('rider/dashboard/', views.rider_dashboard, name='rider_dashboard'),
    path('rider/<int:pk>/accept/', views.accept_ride, name='accept_ride'),
    path('rider/<int:pk>/complete/', views.complete_ride, name='complete_ride'),


]

