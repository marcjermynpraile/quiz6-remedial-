from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views



app_name = 'accounts'

urlpatterns = [
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('signout/', views.signout_view, name='signout'),

]
