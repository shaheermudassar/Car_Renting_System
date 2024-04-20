from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Address, UserProfile, LicenseDetail
from cars.models import Car, Review
from rent.models import Rent, Rented_Car, Extended_Rent
from django.views.decorators.csrf import csrf_protect
import json
import requests

def rent_request_form(request):
    if request.method == "POST":
        request.session['car_id'] = request.POST.get("car_id")
        request.session['period'] = request.POST.get("period")
        request.session['number_of_period'] = request.POST.get("number_of_period")
        return redirect("rent_page")

@login_required
def extend_rent_request_form(request):
    if request.method == "POST":
        request.session['extended_rent_car_id'] = request.POST.get("car_id")
        print(request.session['extended_rent_car_id'])
        request.session['rent_id'] = request.POST.get("rent_id")
        print(request.session['rent_id'])
        request.session['extended_period'] = request.POST.get("period")
        print(request.session['extended_period'])
        request.session['extended_number_of_period'] = request.POST.get("number_of_period")
        print(request.session['extended_number_of_period'])
        return redirect("extended_rent_page")

@login_required
def rent_page(request):
    if 'car_id' in request.session and 'period' in request.session and 'number_of_period' in request.session:
        car_id = request.session['car_id']
        period = request.session['period']
        number_of_period = request.session['number_of_period']
        car = Car.objects.get(id = car_id)
        rent = 0
        if period == "Day":
            rent = int(number_of_period) * int(car.per_day_rent)
        elif period == "Week":
            rent = int(number_of_period) * int(car.weekly_rent)
        elif period == "Month":
            rent = int(number_of_period) * int(car.monthly_rent)
        total_rent = rent + car.security_charges()
        # print(f"time: {number_of_period}, period: {period}, total rent: {total_rent}")
        profile_miss = None
        profile = UserProfile.objects.get(user = request.user)
        if profile.first_name == None or profile.last_name == None or profile.contact == None or profile.cnic == None:
            profile_miss = True
        address_miss = None
        address = Address.objects.get(user=request.user)
        if address.country == None or address.city == None or address.town_or_area == None or address.address == '':
            address_miss = True
        license_miss = None
        license = LicenseDetail.objects.get(user = request.user)
        if license.license_name == None or license.expiry_date == None or license.license_pic == None or license.valid == False:
            license_miss = True
        context = {
            "address_miss": address_miss,
            "profile_miss": profile_miss,
            "license_miss": license_miss,
            "profile": profile,
            "address": address,
            "license": license,
            # rent form data 
            "rent": rent,
            "period": period,
            "number_of_period": number_of_period,
            "total_rent": total_rent,
            "car": car,
        }
        if request.htmx:
            return render(request, "rent/smallComponents/rentPageSmallComponent.html", context)
        else:
            return render(request, "rent/rent_page.html", context)
    else:
        return redirect("home")

@login_required
def extended_rent_page(request):
    if 'extended_rent_car_id' in request.session and 'rent_id' in request.session and 'extended_period' in request.session and 'extended_number_of_period' in request.session:
        car_id = request.session['extended_rent_car_id']
        period = request.session['extended_period']
        rent_id = request.session['rent_id']
        number_of_period = request.session['extended_number_of_period']
        original_rent = Rent.objects.get(rid = rent_id)
        car = Car.objects.get(id = car_id)
        rent = 0
        if period == "Day":
            rent = int(number_of_period) * int(car.per_day_rent)
        elif period == "Week":
            rent = int(number_of_period) * int(car.weekly_rent)
        elif period == "Month":
            rent = int(number_of_period) * int(car.monthly_rent)
        total_rent = rent
        
        context = {
            # rent form data 
            "rent": rent,
            "period": period,
            "number_of_period": number_of_period,
            "total_rent": total_rent,
            "car": car,
            "original_rent": original_rent,
        }
        return render(request, "rent/extended_rent_page.html", context)
    else:
        return redirect("home")

@login_required
def update_profile_form(request):
    profile = UserProfile.objects.get(user = request.user)
    profile.first_name = request.POST.get("first_name") or profile.first_name
    profile.last_name = request.POST.get("last_name") or profile.last_name
    profile.contact = request.POST.get("contact") or profile.contact
    profile.cnic = request.POST.get("cnic") or profile.cnic
    profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
    profile.save()
    return HttpResponseRedirect("rent_page")

@login_required
def update_address_form(request):
    address = Address.objects.get(user=request.user)
    address.country = request.POST.get("country") or address.country
    address.city = request.POST.get("city") or address.city
    address.town_or_area = request.POST.get("town_or_area") or address.town_or_area
    address.address = request.POST.get("address") or address.address
    address.save()
    return HttpResponseRedirect("rent_page")

def update_license_form(request):
    license = LicenseDetail.objects.get(user=request.user)
    license.license_name = request.POST.get("license_name") or license.license_name
    license.expiry_date = request.POST.get("expiry_date") or license.expiry_date
    license.license_pic = request.FILES.get("license_pic") or license.license_pic
    license.valid = True
    license.save()
    return HttpResponseRedirect("rent_page")

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

        your_iframe_id = 166908
            # Step 4: Redirect to PayMob iframe URL
        iframe_url = f"https://pakistan.paymob.com/api/acceptance/iframes/{your_iframe_id}?payment_token={payment_token}"
        print(iframe_url)
        return redirect(iframe_url)


def payment_success(request):
    transaction_data = request.GET
    success_status = transaction_data.get('success', '').lower()
    merchant_order_id = transaction_data.get('merchant_order_id')
    if merchant_order_id.startswith(('1', '2', '3', '4', '5')):
        rent = Rent.objects.get(rid = merchant_order_id)
    elif merchant_order_id.startswith(('6', '7', '8', '9')):
        extended_rent = Extended_Rent.objects.get(erid = merchant_order_id)
        extended_rent_ki_rent_id = extended_rent.rent.rid
        rent = Rent.objects.get(rid = extended_rent_ki_rent_id)
    if success_status == 'true':
        if rent.paid == False:
            rent.paid = True
            rent.save()
            if rent.delivery_method == "Pickup":
                return_status = "To be Picked"
            elif rent.delivery_method == "Home Delivery":
                return_status = "To be delivered"

            if not Rented_Car.objects.filter(rent=rent).exists():
                Rented_Car.objects.create(
                    rent=rent,
                    return_status = return_status,
                )
        elif rent.paid == True:
            extended_rent = Extended_Rent.objects.get(rent = rent)
            extended_rent.confirmed = True
            extended_rent.save()
        context = {
            "rent": rent,
        }
        rent.refresh_from_db()
        return render(request, "rent/payment_success.html", context)
    else:
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