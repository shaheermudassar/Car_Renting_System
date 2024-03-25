from django.urls import path
from users import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile", views.profile, name="profile"),
    path("address", views.address, name="address"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("license_info", views.license_info, name="license_info"),
    # path("license_image_data_generator", views.license_image_data_generator, name="license_image_data_generator"),
    path("license_set_form", views.license_set_form, name="license_set_form"),
    path("rent_detail/<str:rid>", views.rent_detail, name="rent_detail"),
    path("notifications", views.notifications, name="notifications"),

    # HTMX urls
    path("password_check_for_account_deletion", views.password_check_for_account_deletion, name="password_check_for_account_deletion"),
    path("license_info/manual", views.manual_license_set, name="manual_license_set"),

    # full page htmx:
    path("full_dashboard", views.user, name="full_dashboard"),
    path("", views.user, name="user"),
]
