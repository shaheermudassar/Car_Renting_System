from django.urls import path
from core import views  # Import views module from core app

urlpatterns = [
    # Define URL patterns and their corresponding view functions
    path("", views.home, name="home"),  # Home page
    path("car/<id>", views.car_detail, name="car_detail"),  # Car detail page
    path("listing", views.listing, name="listing"),  # Listing page
    path("brands", views.brands, name="brands"),  # Brands page
    path("brands/<str:name>", views.brand_details, name="brand_details"),  # Brand details page
    path("types", views.types, name="types"),  # Types page
    path("types/<str:name>", views.type_details, name="type_details"),  # Type details page
    path("saved", views.saved_cars, name="saved"),  # Saved cars page
    path("contact", views.contact, name="contact"),  # Contact page
    path("ownerboard", views.ownerboard, name="ownerboard"),  # Ownerboard page

    # HTMX views:
    path("save_car_handler", views.save_car_handler, name="save_car_handler"),  # Save car handler view
    path("contact_form", views.contact_form, name="contact_form"),  # Contact form view
    path("total_rent", views.total_rent, name="total_rent"),  # Total rent view
    path("new_cars", views.new_cars, name="new_cars"),  # New cars view
    path("used_cars", views.used_cars, name="used_cars"),  # Used cars view

    # Full component HTMX views:
    path("full_home", views.home, name="full_home"),  # Full home page with components
]
