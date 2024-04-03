from django.shortcuts import render
from django.http import HttpResponse
from cars.models import Car, Brand, Category
from users.models import Saved_Car
from core.filters import CarFilter
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    cars = Car.objects.filter(rented=False)[:8]
    brands = Brand.objects.all()[:10]
    types = Category.objects.all().order_by("id")[:5]
    htmx = False
    if request.htmx:
        htmx = True
    context = {
        "cars": cars,
        "new_cars": new_cars,
        "used_cars": used_cars,
        "brands": brands,
        "types":types,
        "htmx": htmx,
    }
    url_name = request.resolver_match.url_name
    if request.htmx and url_name == 'full_home':
        return render(request, "core/components/homeFullComponent.html", context)
    elif request.htmx:
        return render(request, "core/components/homeComponent.html", context)
    else:
        return render(request, "core/home.html", context)
    
def new_cars(request):
    new_cars = Car.objects.filter(specifications__condition__gt=9, rented=False)[:8]
    return render(request, "core/smallComponents/newCars.html", {"new_cars": new_cars})
    
def used_cars(request):
    used_cars = Car.objects.filter(specifications__condition__lte=9, rented=False)[:8]
    return render(request, "core/smallComponents/usedCars.html", {"used_cars": used_cars})

def car_detail(request, id):
    car = Car.objects.get(id = id)
    car_is_saved = False
    if request.user.is_authenticated and Saved_Car.objects.filter(user=request.user, car=car).exists():
        car_is_saved = True
    related_cars = Car.objects.filter(Q(category=car.category, rented=False) | Q(brand=car.brand, rented = False))[:7]
    context = {
        "car": car,
        "car_is_saved": car_is_saved,
        "related_cars": related_cars,
    }
    if request.htmx:
        return render(request, "core/components/car_detailsComponent.html", context)
    else:
        return render(request, "core/car_details.html", context)


def listing(request):
    car_filter = CarFilter(request.GET, queryset=Car.objects.filter(rented=False))
    # Set the number of items to display per page
    items_per_page = 8
    paginator = Paginator(car_filter.qs, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, display the first page
        items = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results
        items = paginator.page(paginator.num_pages)
    context = {
        "form_s": car_filter.form,
        "filtered_cars": items,
        "search": car_filter.form.cleaned_data.get('name_first', '') or car_filter.form.cleaned_data.get('name_second', ''),
    }
    if request.htmx:
        return render(request, "core/components/listingComponent.html", context)
    else:
        return render(request, "core/listing.html", context)

def brands(request):
    brands = Brand.objects.all()
    context = {
        "brands": brands,
    }
    if request.htmx:
        return render(request, "core/components/brandsComponent.html", context)
    else:
        return render(request, "core/brands.html", context)

def brand_details(request, name):
    brand = Brand.objects.get(name=name)
    cars = Car.objects.filter(brand=brand, rented = False)
    context = {
        "cars": cars,
        "brand": brand,
    }
    if request.htmx:
        return render(request, "core/components/brand_detailsComponent.html", context)
    else:
        return render(request, "core/brand_details.html", context)

def types(request):
    types = Category.objects.all()
    context = {
        "types": types,
    }
    if request.htmx:
        return render(request, "core/components/typesComponent.html", context)
    else:    
        return render(request, "core/types.html", context)

def type_details(request, name):
    category = Category.objects.get(name=name)
    cars = Car.objects.filter(category = category, rented = False)
    context = {
        "cars": cars,
        "category": category,
    }
    if request.htmx:
        return render(request, "core/components/type_detailsComponent.html", context)
    else:
        return render(request, "core/type_details.html", context)

@login_required
def saved_cars(request):
    saved_cars = Saved_Car.objects.filter(user=request.user)
    cars = [saved_car.car for saved_car in saved_cars]
    context = {
        "cars": cars,
    }
    if request.htmx:
        return render(request, "core/components/savedComponent.html", context)
    else:
        return render(request, "core/saved.html", context)
    
@login_required
@csrf_exempt
def save_car_handler(request):
    car_id = request.POST.get("car_id")
    _car = Car.objects.get(id = car_id)
    unsave_button = """ <button type="submit" name="unsave" class="bg-white list-type-banner d-inline-flex align-items-center mytext2">
                <img src="/static/images/hearted.png" alt="" width="25px" class="mr-2" />
                <div class="inner">
                  <h4 class="title text-black font-bold py-2" style="font-weight: 600;">Saved</h4>
                </div>
              </button> """
    save_button = """ <button type="submit" name="save" class="bg-white list-type-banner d-inline-flex align-items-center mytext2">
                <img src="/static/images/heart.png" alt="" width="25px" class="mr-2" />
                <div class="inner">
                  <h4 class="title text-black font-bold py-2" style="font-weight: 600;">Save</h4>
                </div>
              </button> """
    if "save" in request.POST:
        Saved_Car.objects.create(
            user = request.user,
            car = _car
        )
        return HttpResponse(unsave_button)
    elif "unsave" in request.POST:
        car_to_be_deleted = Saved_Car.objects.get(
            user = request.user,
            car = _car
        )
        car_to_be_deleted.delete()
        return HttpResponse(save_button)
    
def contact(request):
    if request.htmx:
        return render(request, "core/components/contactComponent.html")
    else:
        return render(request, "core/contact.html")

@login_required
def contact_form(request):
    if request.method == "POST":
        message = request.POST.get("message")
        subject = f"DaisyRoom Contact Mail from {request.user.username} "
        body = message
        sender_email = request.user.email
        recipient_email = 'shaheer.mudassar13@gmail.com'
        send_mail(subject, body, sender_email, [recipient_email])
        return HttpResponse("Mail sent ✔")
    
def total_rent(request):
    selected_value = request.GET.get("selected_value")
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
    response = f'<input type="hidden" name="period" value="{period}"> <input type="hidden" name="number_of_period" value="{number_of_period}"> <button type="submit" class="mt-4 btn bg-[#570df8]" data-te-ripple-init data-te-ripple-color="light">Continue</button>'
    return HttpResponse(response)

def ownerboard(request):
    return render(request, "owner/ownerboard.html")