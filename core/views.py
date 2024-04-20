from django.shortcuts import render  # Import render function to render templates
from django.http import HttpResponse  # Import HttpResponse to generate HTTP responses
from cars.models import Car, Brand, Category  # Import Car, Brand, and Category models
from users.models import Saved_Car  # Import Saved_Car model
from core.filters import CarFilter  # Import CarFilter from core.filters
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt decorator
from django.core.mail import send_mail  # Import send_mail function for sending emails
from django.db.models import Q  # Import Q for complex queries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator for pagination


def home(request):
    # Retrieve 8 cars that are not rented
    cars = Car.objects.filter(rented=False)[:8]
    # Retrieve all brands and limit to 10
    brands = Brand.objects.all()[:10]
    # Retrieve all categories and limit to 5
    types = Category.objects.all().order_by("id")[:5]
    htmx = False  # Initialize htmx flag to False
    # Check if request is htmx
    if request.htmx:
        htmx = True
    # Context for rendering template
    context = {
        "cars": cars,
        "brands": brands,
        "types": types,
        "htmx": htmx,
    }
    # Check current URL name
    url_name = request.resolver_match.url_name
    # Render appropriate template based on htmx flag and URL name
    if request.htmx and url_name == 'full_home':
        return render(request, "core/components/homeFullComponent.html", context)
    elif request.htmx:
        return render(request, "core/components/homeComponent.html", context)
    else:
        return render(request, "core/home.html", context)


def new_cars(request):
    # Retrieve 8 new cars that are not rented
    new_cars = Car.objects.filter(specifications__condition__gt=9, rented=False)[:8]
    # Render template with new cars
    return render(request, "core/smallComponents/newCars.html", {"new_cars": new_cars})


def used_cars(request):
    # Retrieve 8 used cars that are not rented
    used_cars = Car.objects.filter(specifications__condition__lte=9, rented=False)[:8]
    # Render template with used cars
    return render(request, "core/smallComponents/usedCars.html", {"used_cars": used_cars})


def car_detail(request, id):
    # Retrieve car details based on ID
    car = Car.objects.get(id=id)
    # Check if the car is saved by the current user
    car_is_saved = False
    if request.user.is_authenticated and Saved_Car.objects.filter(user=request.user, car=car).exists():
        car_is_saved = True
    # Retrieve related cars based on category or brand
    related_cars = Car.objects.filter(Q(category=car.category, rented=False) | Q(brand=car.brand, rented=False))[:7]
    # Context for rendering template
    context = {
        "car": car,
        "car_is_saved": car_is_saved,
        "related_cars": related_cars,
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/car_detailsComponent.html", context)
    else:
        return render(request, "core/car_details.html", context)


def listing(request):
    # Initialize CarFilter with request GET parameters and queryset of available cars
    car_filter = CarFilter(request.GET, queryset=Car.objects.filter(rented=False))
    # Set the number of items to display per page
    items_per_page = 8
    paginator = Paginator(car_filter.qs, items_per_page)
    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')
    try:
        # Get items for the current page
        items = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, display the first page
        items = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page of results
        items = paginator.page(paginator.num_pages)
    # Context for rendering template
    context = {
        "form_s": car_filter.form,
        "filtered_cars": items,
        "search": car_filter.form.cleaned_data.get('name_first', '') or car_filter.form.cleaned_data.get('name_second', ''),
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/listingComponent.html", context)
    else:
        return render(request, "core/listing.html", context)


def brands(request):
    # Retrieve all brands
    brands = Brand.objects.all()
    # Context for rendering template
    context = {
        "brands": brands,
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/brandsComponent.html", context)
    else:
        return render(request, "core/brands.html", context)


def brand_details(request, name):
    # Retrieve brand details based on name
    brand = Brand.objects.get(name=name)
    # Retrieve cars associated with the brand
    cars = Car.objects.filter(brand=brand, rented=False)
    # Context for rendering template
    context = {
        "cars": cars,
        "brand": brand,
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/brand_detailsComponent.html", context)
    else:
        return render(request, "core/brand_details.html", context)


def types(request):
    # Retrieve all categories
    types = Category.objects.all()
    # Context for rendering template
    context = {
        "types": types,
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/typesComponent.html", context)
    else:
        return render(request, "core/types.html", context)


def type_details(request, name):
    # Retrieve category details based on name
    category = Category.objects.get(name=name)
    # Retrieve cars associated with the category
    cars = Car.objects.filter(category=category, rented=False)
    # Context for rendering template
    context = {
        "cars": cars,
        "category": category,
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/type_detailsComponent.html", context)
    else:
        return render(request, "core/type_details.html", context)


@login_required
def saved_cars(request):
    # Retrieve cars saved by the current user
    saved_cars = Saved_Car.objects.filter(user=request.user)
    # Extract cars from Saved_Car instances
    cars = [saved_car.car for saved_car in saved_cars]
    # Context for rendering template
    context = {
        "cars": cars,
    }
    # Render appropriate template based on htmx flag
    if request.htmx:
        return render(request, "core/components/savedComponent.html", context)
    else:
        return render(request, "core/saved.html", context)


@login_required
@csrf_exempt
def save_car_handler(request):
    # Extract car ID from POST request
    car_id = request.POST.get("car_id")
    # Retrieve Car object based on ID
    _car = Car.objects.get(id=car_id)
    # HTML button code for saving a car
    unsave_button = """
    <button type="submit" name="unsave" class="bg-white list-type-banner d-inline-flex align-items-center mytext2">
        <img src="/static/images/hearted.png" alt="" width="25px" class="mr-2" />
        <div class="inner">
            <h4 class="title text-black font-bold py-2" style="font-weight: 600;">Saved</h4>
        </div>
    </button>
    """
    # HTML button code for unsaving a car
    save_button = """
    <button type="submit" name="save" class="bg-white list-type-banner d-inline-flex align-items-center mytext2">
        <img src="/static/images/heart.png" alt="" width="25px" class="mr-2" />
        <div class="inner">
            <h4 class="title text-black font-bold py-2" style="font-weight: 600;">Save</h4>
        </div>
    </button>
    """
    # Check if the "save" button is in the POST request
    if "save" in request.POST:
        # Save the car for the current user
        Saved_Car.objects.create(
            user=request.user,
            car=_car
        )
        # Return HTML for the "unsave" button as an HTTP response
        return HttpResponse(unsave_button)
    elif "unsave" in request.POST:
        # Find the Saved_Car instance to delete
        car_to_be_deleted = Saved_Car.objects.get(
            user=request.user,
            car=_car
        )
        # Delete the Saved_Car instance
        car_to_be_deleted.delete()
        # Return HTML for the "save" button as an HTTP response
        return HttpResponse(save_button)


def contact(request):
    # Render contact template
    if request.htmx:
        return render(request, "core/components/contactComponent.html")
    else:
        return render(request, "core/contact.html")


@login_required
def contact_form(request):
    # Handle contact form submission
    if request.method == "POST":
        # Retrieve message from POST request
        message = request.POST.get("message")
        # Construct email subject
        subject = f"DaisyRoom Contact Mail from {request.user.username} "
        # Set email body to the message
        body = message
        # Set sender's email to current user's email
        sender_email = request.user.email
        # Set recipient's email (can be changed to desired recipient)
        recipient_email = 'shaheer.mudassar13@gmail.com'
        # Send email using send_mail function
        send_mail(subject, body, sender_email, [recipient_email])
        # Return success message as HTTP response
        return HttpResponse("Mail sent ✔")


def total_rent(request):
    # Get selected value from GET request
    selected_value = request.GET.get("selected_value")
    # Initialize period and number_of_period
    if selected_value == "1_day":
        period = "Day"
        number_of_period = 1
    elif selected_value == "2_day":
        period = "Day"
        number_of_period = 2
    elif selected_value == "3_day":
        period = "Day"
        number_of_period = 3
    elif selected_value == "4_day":
        period = "Day"
        number_of_period = 4
    elif selected_value == "5_day":
        period = "Day"
        number_of_period = 5
    elif selected_value == "6_day":
        period = "Day"
        number_of_period = 6
    elif selected_value == "1_week":
        period = "Week"
        number_of_period = 1
    elif selected_value == "2_week":
        period = "Week"
        number_of_period = 2
    elif selected_value == "3_week":
        period = "Week"
        number_of_period = 3
    elif selected_value == "1_month":
        period = "Month"
        number_of_period = 1
    elif selected_value == "2_month":
        period = "Month"
        number_of_period = 2
    elif selected_value == "3_month":
        period = "Month"
        number_of_period = 3
    elif selected_value == "6_month":
        period = "Month"
        number_of_period = 6
    elif selected_value == "12_month":
        period = "Month"
        number_of_period = 12
    else:
        period = "error"
        number_of_period = 500
    # Construct HTML response
    response = f'<input type="hidden" name="period" value="{period}"> <input type="hidden" name="number_of_period" value="{number_of_period}"> <button type="submit" class="mt-4 btn bg-[#570df8]" data-te-ripple-init data-te-ripple-color="light">Continue</button>'
    # Return HTML response
    return HttpResponse(response)


def ownerboard(request):
    # Render ownerboard template
    return render(request, "owner/ownerboard.html")
