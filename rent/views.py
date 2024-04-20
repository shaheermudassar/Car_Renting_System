from django.shortcuts import render, redirect  # Importing necessary functions and modules from Django
from django.http import HttpResponseRedirect, HttpResponse  # Importing necessary HTTP response-related modules
from django.contrib.auth.decorators import login_required  # Importing the login_required decorator
from users.models import Address, UserProfile, LicenseDetail  # Importing necessary models from the users app
from cars.models import Car, Review  # Importing necessary models from the cars app
from rent.models import Rent, Rented_Car, Extended_Rent  # Importing necessary models from the rent app
from django.views.decorators.csrf import csrf_protect  # Importing the csrf_protect decorator
import json  # Importing the json module
import requests  # Importing the requests module

# Function to handle the rent request form
def rent_request_form(request):
    if request.method == "POST":  # Check if the request method is POST
        # Store the selected car ID, period, and number of periods in session variables
        request.session['car_id'] = request.POST.get("car_id")
        request.session['period'] = request.POST.get("period")
        request.session['number_of_period'] = request.POST.get("number_of_period")
        return redirect("rent_page")  # Redirect the user to the rent page

# Function to handle the extension of rent request form
@login_required  # Ensures that only logged-in users can access this view
def extend_rent_request_form(request):
    if request.method == "POST":  # Check if the request method is POST
        # Store the selected car ID, rent ID, extended period, and number of periods in session variables
        request.session['extended_rent_car_id'] = request.POST.get("car_id")
        request.session['rent_id'] = request.POST.get("rent_id")
        request.session['extended_period'] = request.POST.get("period")
        request.session['extended_number_of_period'] = request.POST.get("number_of_period")
        return redirect("extended_rent_page")  # Redirect the user to the extended rent page

# Function to handle the rent page
@login_required  # Ensures that only logged-in users can access this view
def rent_page(request):
    if 'car_id' in request.session and 'period' in request.session and 'number_of_period' in request.session:
        # Retrieve car ID, period, and number of periods from session variables
        car_id = request.session['car_id']
        period = request.session['period']
        number_of_period = request.session['number_of_period']
        # Retrieve car object based on the car ID
        car = Car.objects.get(id=car_id)
        rent = 0  # Initialize rent variable
        # Calculate rent based on period and number of periods
        if period == "Day":
            rent = int(number_of_period) * int(car.per_day_rent)
        elif period == "Week":
            rent = int(number_of_period) * int(car.weekly_rent)
        elif period == "Month":
            rent = int(number_of_period) * int(car.monthly_rent)
        total_rent = rent + car.security_charges()  # Calculate total rent
        # Check if user profile, address, and license details are missing
        profile_miss = None
        profile = UserProfile.objects.get(user=request.user)
        if profile.first_name == None or profile.last_name == None or profile.contact == None or profile.cnic == None:
            profile_miss = True
        address_miss = None
        address = Address.objects.get(user=request.user)
        if address.country == None or address.city == None or address.town_or_area == None or address.address == '':
            address_miss = True
        license_miss = None
        license = LicenseDetail.objects.get(user=request.user)
        if license.license_name == None or license.expiry_date == None or license.license_pic == None or license.valid == False:
            license_miss = True
        # Prepare context data for rendering the template
        context = {
            "address_miss": address_miss,
            "profile_miss": profile_miss,
            "license_miss": license_miss,
            "profile": profile,
            "address": address,
            "license": license,
            "rent": rent,  # Rent form data
            "period": period,
            "number_of_period": number_of_period,
            "total_rent": total_rent,
            "car": car,
        }
        if request.htmx:  # Check if the request is an HTMX request
            return render(request, "rent/smallComponents/rentPageSmallComponent.html", context)  # Render small component for HTMX request
        else:
            return render(request, "rent/rent_page.html", context)  # Render full page for non-HTMX request
    else:
        return redirect("home")  # Redirect to the home page if session variables are missing

@login_required  # Ensures that only logged-in users can access this view
def extended_rent_page(request):
    if 'extended_rent_car_id' in request.session and 'rent_id' in request.session and 'extended_period' in request.session and 'extended_number_of_period' in request.session:
        # Retrieve session variables
        car_id = request.session['extended_rent_car_id']
        period = request.session['extended_period']
        rent_id = request.session['rent_id']
        number_of_period = request.session['extended_number_of_period']
        # Retrieve original rent object based on the rent ID
        original_rent = Rent.objects.get(rid=rent_id)
        # Retrieve car object based on the car ID
        car = Car.objects.get(id=car_id)
        rent = 0  # Initialize rent variable
        # Calculate rent based on period and number of periods
        if period == "Day":
            rent = int(number_of_period) * int(car.per_day_rent)
        elif period == "Week":
            rent = int(number_of_period) * int(car.weekly_rent)
        elif period == "Month":
            rent = int(number_of_period) * int(car.monthly_rent)
        total_rent = rent  # Set total rent
        # Prepare context data for rendering the template
        context = {
            "rent": rent,  # Rent form data
            "period": period,
            "number_of_period": number_of_period,
            "total_rent": total_rent,
            "car": car,
            "original_rent": original_rent,
        }
        return render(request, "rent/extended_rent_page.html", context)  # Render the extended rent page
    else:
        return redirect("home")  # Redirect to the home page if session variables are missing

# View function for updating user profile information
@login_required  # Ensures that only logged-in users can access this view
def update_profile_form(request):
    profile = UserProfile.objects.get(user=request.user)  # Retrieve user profile object
    # Update profile fields based on form data or keep existing values
    profile.first_name = request.POST.get("first_name") or profile.first_name
    profile.last_name = request.POST.get("last_name") or profile.last_name
    profile.contact = request.POST.get("contact") or profile.contact
    profile.cnic = request.POST.get("cnic") or profile.cnic
    profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
    profile.save()  # Save the updated profile
    return HttpResponseRedirect("rent_page")  # Redirect to the rent page

# View function for updating user address information
@login_required  # Ensures that only logged-in users can access this view
def update_address_form(request):
    address = Address.objects.get(user=request.user)  # Retrieve user address object
    # Update address fields based on form data or keep existing values
    address.country = request.POST.get("country") or address.country
    address.city = request.POST.get("city") or address.city
    address.town_or_area = request.POST.get("town_or_area") or address.town_or_area
    address.address = request.POST.get("address") or address.address
    address.save()  # Save the updated address
    return HttpResponseRedirect("rent_page")  # Redirect to the rent page

# View function for updating user license information
def update_license_form(request):
    license = LicenseDetail.objects.get(user=request.user)  # Retrieve user license detail object
    # Update license fields based on form data or keep existing values
    license.license_name = request.POST.get("license_name") or license.license_name
    license.expiry_date = request.POST.get("expiry_date") or license.expiry_date
    license.license_pic = request.FILES.get("license_pic") or license.license_pic
    license.valid = True  # Set license as valid
    license.save()  # Save the updated license
    return HttpResponseRedirect("rent_page")  # Redirect to the rent page

@login_required
def process_payment(request):
    if request.method == "POST" and "extend_rent" in request.POST:
        total_rent = request.POST.get("total_rent")
        car_id = request.POST.get("car_id")
        rent_id = request.POST.get("original_rent_id")
        period = request.POST.get("period")
        number_of_period = request.POST.get("number_of_period")
        rent = Rent.objects.get(rid = rent_id)
        car = Car.objects.get(id = car_id)
        extended_rent = Extended_Rent.objects.create(
            rent = rent,
            period = period,
            number_of_period = number_of_period
        )
        extended_rent.save()

        user = UserProfile.objects.get(user=request.user)
        address = Address.objects.get(user=request.user)
        api_key = 'ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRNMk9URTNMQ0p1WVcxbElqb2lNVGN3T0RjeE1qWTROeTQwTURZMk1pSjkuQ0pwSTQ2OUpQWEpEYTZSVklEdzlycERSWjhhUUlsXzEwV2lPZkN1VVJvODQ5Y0lmNGFoZGVLcGNETV9Ea3BNaFFBN1EweTVxSGJ0MzlRLS1fV0tOMHc='

        # Step 1: Authentication Request
        auth_url = 'https://pakistan.paymob.com/api/auth/tokens'
        auth_data = {'api_key': api_key}
        auth_response = requests.post(auth_url, json=auth_data)

        auth_token = auth_response.json()['token']

        order_url = 'https://pakistan.paymob.com/api/ecommerce/orders'
        order_data = {
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": int(total_rent) * 100,
            "currency": "PKR",
            "merchant_order_id": extended_rent.erid,
            "items": [
                {
                    "name": rent.car.name,
                    "amount_cents": int(rent.rent) * 100,
                    "description": "N/A",
                    "quantity": "1"
                },
                ],
            "shipping_data": {
                "apartment": "803", 
                "email": user.user.email, 
                "floor": "42", 
                "first_name": user.first_name, 
                "street": address.town_or_area, 
                "building": "8028", 
                "phone_number": user.contact, 
                "postal_code": "01898", 
                "extra_description": "8 Ram , 128 Giga",
                "city": address.city, 
                "country": address.country, 
                "last_name": user.last_name, 
                "state": "Utah"
            },
                "shipping_details": {
                    "notes" : " test",
                    "number_of_packages": 1,
                    "weight" : 1,
                    "weight_unit" : "Kilogram",
                    "length" : 1,
                    "width" :1,
                    "height" :1,
                    "contents" : "product of some sorts"
                }
            }
        order_response = requests.post(order_url, json=order_data)
        print(order_response.text)
        order_id = order_response.json()['id']

        payment_key_url = "https://pakistan.paymob.com/api/acceptance/payment_keys"
        payment_key_data = {
        "auth_token": auth_token,
        "amount_cents": int(total_rent) * 100, 
        "expiration": 3600, 
        "order_id": order_id,
        "billing_data": {
            "apartment": "N/A", 
            "email": rent.user.email, 
            "floor": "N/A", 
            "first_name": user.first_name, 
            "street": address.town_or_area, 
            "building": "N/A", 
            "phone_number": user.contact, 
            "shipping_method": "PKG", 
            "postal_code": "N/A", 
            "city": address.city, 
            "country": address.country, 
            "last_name": user.last_name, 
            "state": "N/A"
        }, 
        "currency": "PKR", 
        "integration_id": 156651,
        "lock_order_when_paid": "false"
        }
        payment_key_response = requests.post(payment_key_url, json=payment_key_data)
        payment_token = payment_key_response.json()['token']

        your_iframe_id = 166908
            # Step 4: Redirect to PayMob iframe URL
        iframe_url = f"https://pakistan.paymob.com/api/acceptance/iframes/{your_iframe_id}?payment_token={payment_token}"
        print(iframe_url)
        return redirect(iframe_url)
    elif request.method == "POST":
        total_rent = request.POST.get("total_rent")
        car_id = request.POST.get("car_id")
        rent = request.POST.get("rent")
        period = request.POST.get("period")
        delivery_method = request.POST.get("delivery_method")
        number_of_period = request.POST.get("number_of_period")
        car = Car.objects.get(id = car_id)
        
        new_rent = Rent.objects.create(
            user = request.user,
            car = car,
            delivery_method = delivery_method,
            period = period,
            number_of_period = number_of_period,
            rent = rent,
            total_rent = total_rent
        )
        new_rent.save()

        user = UserProfile.objects.get(user=request.user)
        address = Address.objects.get(user=request.user)
        api_key = 'ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRNMk9URTNMQ0p1WVcxbElqb2lNVGN3T0RjeE1qWTROeTQwTURZMk1pSjkuQ0pwSTQ2OUpQWEpEYTZSVklEdzlycERSWjhhUUlsXzEwV2lPZkN1VVJvODQ5Y0lmNGFoZGVLcGNETV9Ea3BNaFFBN1EweTVxSGJ0MzlRLS1fV0tOMHc='

        # Step 1: Authentication Request
        auth_url = 'https://pakistan.paymob.com/api/auth/tokens'
        auth_data = {'api_key': api_key}
        auth_response = requests.post(auth_url, json=auth_data)

        auth_token = auth_response.json()['token']

        order_url = 'https://pakistan.paymob.com/api/ecommerce/orders'
        order_data = {
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": int(new_rent.total_rent) * 100,
            "currency": "PKR",
            "merchant_order_id": new_rent.rid,
            "items": [
                {
                    "name": new_rent.car.name,
                    "amount_cents": int(new_rent.rent) * 100,
                    "description": "N/A",
                    "quantity": "1"
                },
                ],
            "shipping_data": {
                "apartment": "803", 
                "email": user.user.email, 
                "floor": "42", 
                "first_name": user.first_name, 
                "street": address.town_or_area, 
                "building": "8028", 
                "phone_number": user.contact, 
                "postal_code": "01898", 
                "extra_description": "8 Ram , 128 Giga",
                "city": address.city, 
                "country": address.country, 
                "last_name": user.last_name, 
                "state": "Utah"
            },
                "shipping_details": {
                    "notes" : " test",
                    "number_of_packages": 1,
                    "weight" : 1,
                    "weight_unit" : "Kilogram",
                    "length" : 1,
                    "width" :1,
                    "height" :1,
                    "contents" : "product of some sorts"
                }
            }
        order_response = requests.post(order_url, json=order_data)
        print(order_response.text)
        order_id = order_response.json()['id']

        payment_key_url = "https://pakistan.paymob.com/api/acceptance/payment_keys"
        payment_key_data = {
        "auth_token": auth_token,
        "amount_cents": int(new_rent.total_rent) * 100, 
        "expiration": 3600, 
        "order_id": order_id,
        "billing_data": {
            "apartment": "N/A", 
            "email": new_rent.user.email, 
            "floor": "N/A", 
            "first_name": user.first_name, 
            "street": address.town_or_area, 
            "building": "N/A", 
            "phone_number": user.contact, 
            "shipping_method": "PKG", 
            "postal_code": "N/A", 
            "city": address.city, 
            "country": address.country, 
            "last_name": user.last_name, 
            "state": "N/A"
        }, 
        "currency": "PKR", 
        "integration_id": 156651,
        "lock_order_when_paid": "false"
        }
        payment_key_response = requests.post(payment_key_url, json=payment_key_data)
        payment_token = payment_key_response.json()['token']

            # Step 4: Redirect to PayMob iframe URL
        iframe_url = f"https://pakistan.paymob.com/api/acceptance/iframes/{your_iframe_id}?payment_token={payment_token}"
        print(iframe_url)
        return redirect(iframe_url)

       

def payment_success(request):
    # Extract transaction data from the GET request
    transaction_data = request.GET
    
    # Retrieve the success status from transaction data and convert it to lowercase
    success_status = transaction_data.get('success', '').lower()
    
    # Extract the merchant order ID from transaction data
    merchant_order_id = transaction_data.get('merchant_order_id')
    
    # Check if the merchant order ID starts with digits 1 to 5 (indicating a regular rent)
    if merchant_order_id.startswith(('1', '2', '3', '4', '5')):
        # Retrieve the rent object associated with the merchant order ID
        rent = Rent.objects.get(rid=merchant_order_id)
    
    # Check if the merchant order ID starts with digits 6 to 9 (indicating an extended rent)
    elif merchant_order_id.startswith(('6', '7', '8', '9')):
        # Retrieve the extended rent object associated with the merchant order ID
        extended_rent = Extended_Rent.objects.get(erid=merchant_order_id)
        # Retrieve the original rent ID associated with the extended rent
        original_rent_id = extended_rent.rent.rid
        # Retrieve the original rent object using the original rent ID
        rent = Rent.objects.get(rid=original_rent_id)
    
    # Check if the payment was successful
    if success_status == 'true':
        # If the rent is not yet paid
        if rent.paid == False:
            # Mark the rent as paid
            rent.paid = True
            rent.save()
            # Determine the return status based on the delivery method
            if rent.delivery_method == "Pickup":
                return_status = "To be Picked"
            elif rent.delivery_method == "Home Delivery":
                return_status = "To be delivered"
            
            # If the rented car object does not exist, create one
            if not Rented_Car.objects.filter(rent=rent).exists():
                Rented_Car.objects.create(
                    rent=rent,
                    return_status=return_status,
                )
        # If the rent is already paid (for extended rent)
        elif rent.paid == True:
            # Mark the extended rent as confirmed
            extended_rent = Extended_Rent.objects.get(rent=rent)
            extended_rent.confirmed = True
            extended_rent.save()
        
        # Prepare the context to be rendered in the template
        context = {
            "rent": rent,
        }
        
        # Refresh the rent object from the database
        rent.refresh_from_db()
        
        # Render the payment success template with the context
        return render(request, "rent/payment_success.html", context)
    
    # If the payment was not successful
    else:
        # Render the payment failed template
        return render(request, "rent/payment_failed.html")


def success_mail(request):
    return render(request, "rent/order_success_mail.html")

def review_add(request):
    car_id = request.POST.get("car_id")
    print(car_id)
    car = Car.objects.get(id = car_id)
    Review.objects.create(
        user = request.user,
        car = car,
        rating = request.POST.get("rating-2"),
        review = request.POST.get("review"),
    )
    return HttpResponse('<a class="m-4 btn bg-[#570df8] hover:bg-[black]"> Review Added ✓ <i class="fa-solid fa-arrow-right ml-2"></i></a>')