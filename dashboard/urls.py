from django.urls import path
from .views import users_list, add_balance, dashboard_home  #
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='index'),
    path('users/', users_list, name='users'),
    path('add-balance/', add_balance, name='add_balance'),
    path('', views.index, name='index'),

]

