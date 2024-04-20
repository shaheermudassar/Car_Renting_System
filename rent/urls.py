from django.urls import path
from . import views

urlpatterns = [
     path("rent_page", views.rent_page, name="rent_page"),
     path("extended_rent_page", views.extended_rent_page, name="extended_rent_page"),
     path("success_mail", views.success_mail, name="success_mail"),

     #forms:
     path("rent_request_form", views.rent_request_form, name="rent_request_form"),
     path("extend_rent_request_form", views.extend_rent_request_form, name="extend_rent_request_form"),
     path("process_payment", views.process_payment, name="process_payment"),
     path("payment", views.payment_success, name="payment_success"),
     path("review_add", views.review_add, name="review_add"),


     # htmx views:
     path("update_profile_form", views.update_profile_form, name="update_profile_form"),
     path("update_address_form", views.update_address_form, name="update_address_form"),
     path("update_license_form", views.update_license_form, name="update_license_form"),
]
