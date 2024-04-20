from django.urls import path
from users import views

urlpatterns = [
    # Paths for regular views
    path("dashboard", views.dashboard, name="dashboard"),  # URL for the user dashboard
    path("profile", views.profile, name="profile"),  # URL for the user profile page
    path("address", views.address, name="address"),  # URL for updating user address
    path("delete_account", views.delete_account, name="delete_account"),  # URL for deleting user account
    path("license_info", views.license_info, name="license_info"),  # URL for displaying license information
    # path("license_image_data_generator", views.license_image_data_generator, name="license_image_data_generator"),
    path("license_set_form", views.license_set_form, name="license_set_form"),  # URL for handling license form submission
    path("rent_detail/<str:rid>", views.rent_detail, name="rent_detail"),  # URL for displaying rent details
    path("notifications", views.notifications, name="notifications"),  # URL for displaying notifications
    
    # HTMX URLs
    path("password_check_for_account_deletion", views.password_check_for_account_deletion, name="password_check_for_account_deletion"),  # URL for checking password during account deletion
    path("license_info/manual", views.manual_license_set, name="manual_license_set"),  # URL for manually setting license details
    
    # Full page HTMX URLs
    path("full_dashboard", views.user, name="full_dashboard"),  # URL for full dashboard (HTMX)
    path("", views.user, name="user"),  # Default user URL
]
