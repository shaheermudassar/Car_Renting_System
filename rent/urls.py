from django.urls import path
from . import views

urlpatterns = [
    # Regular views
    path("rent_page", views.rent_page, name="rent_page"),  # Renders the rent page
    path("extended_rent_page", views.extended_rent_page, name="extended_rent_page"),  # Renders the extended rent page
    path("success_mail", views.success_mail, name="success_mail"),  # Success email view

    # Forms handling views
    path("rent_request_form", views.rent_request_form, name="rent_request_form"),  # Handles rent request form submission
    path("extend_rent_request_form", views.extend_rent_request_form, name="extend_rent_request_form"),  # Handles extended rent request form submission
    path("process_payment", views.process_payment, name="process_payment"),  # Handles payment processing
    path("payment", views.payment_success, name="payment_success"),  # Handles payment success
    
    # Review related views
    path("review_add", views.review_add, name="review_add"),  # Adds a review

    # HTMX views
    path("update_profile_form", views.update_profile_form, name="update_profile_form"),  # Updates user profile form
    path("update_address_form", views.update_address_form, name="update_address_form"),  # Updates address form
    path("update_license_form", views.update_license_form, name="update_license_form"),  # Updates license form
]
