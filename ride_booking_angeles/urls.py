from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls','accounts'), namespace='accounts')),
    path('rides/', include(('rides.urls','rides'), namespace='rides')),
    path('dashboard/', include('dashboard.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),



]
