from django.urls import path
from core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("car/<id>", views.car_detail, name="car_detail"),
    path("listing", views.listing, name="listing"),
    path("brands", views.brands, name="brands"),
    path("brands/<str:name>", views.brand_details, name="brand_details"),
    path("types", views.types, name="types"),
    path("types/<str:name>", views.type_details, name="type_details"),
    path("saved", views.saved_cars, name="saved"),
    path("contact", views.contact, name="contact"),
    path("ownerboard", views.ownerboard, name="ownerboard"),

    # htmx views:
    path("save_car_handler", views.save_car_handler, name="save_car_handler"),
    path("contact_form", views.contact_form, name="contact_form"),
    path("total_rent", views.total_rent, name="total_rent"),
    path("new_cars", views.new_cars, name="new_cars"),
    path("used_cars", views.used_cars, name="used_cars"),

    # full component htmx:
    path("full_home", views.home, name="full_home"),
]
