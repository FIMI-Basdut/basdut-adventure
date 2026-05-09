from django.urls import path
from dashboard.views import show_dashboard_customer, show_dashboard_organizer, show_dashboard_admin, show_profile_customer, show_profile_organizer


app_name = 'dashboard'


urlpatterns = [
    path('customer/', show_dashboard_customer, name='dashboard_customer'),
    path('organizer/', show_dashboard_organizer, name='dashboard_organizer'),
    path('admin/', show_dashboard_admin, name='dashboard_admin'),
    path('customer/profile/', show_profile_customer, name='profile_customer'),
    path('organizer/profile/', show_profile_organizer, name='profile_organizer'),

]