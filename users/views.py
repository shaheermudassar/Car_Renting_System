from django.shortcuts import render, redirect
from userauths.models import User
from users.models import UserProfile, Address, LicenseDetail, Notification
from cars.models import Review, Car
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
# from easyocr import Reader
# import re, os
from datetime import datetime
from django.utils import timezone
from rent.models import Rent, Rented_Car
from django.contrib import messages

@login_required
def user(request):
    url_name = request.resolver_match.url_name
    if request.htmx and url_name == 'full_dashboard':
        return render(request, "users/components/fulldashboardComponent.html")
    elif request.htmx:
        return render(request, "users/components/userComponent.html")
    else:
        return render(request, "users/user.html")
@login_required
def dashboard(request):
    rents = Rented_Car.objects.filter(rent__user = request.user).order_by("-id")
    context = {
        "rents": rents,
    }
    if request.htmx:
        return render(request, "users/components/dashboardComponent.html", context)
    else:
        return render(request, "users/dashboard.html", context)

from rent.models import Extended_Rent
@login_required
def rent_detail(request, rid):
    reviewed = False
    rent = Rent.objects.get(rid = rid)
    extended_rent = False
    if Extended_Rent.objects.filter(rent = rent).exists():
        extended_rent = True
    car_id = rent.car.id
    car = Car.objects.get(id = car_id)
    if Review.objects.filter(user = request.user, car = car).exists():
        reviewed = True
    context = {
        "rent": rent,
        "reviewed": reviewed,
        "extended_rent": extended_rent,
    }
    if request.htmx:
        return render(request, "users/components/rent_detailComponent.html", context)
    else:
        return render(request, "users/rent_detail.html", context)

@login_required
def profile(request):
    
    profile = UserProfile.objects.get(user = request.user)
    context = {
        "profile": profile,
        
    }
    if request.method == 'POST':
        profile.first_name = request.POST.get("first_name")    
        profile.last_name = request.POST.get("last_name")       
        profile.cnic = request.POST.get("cnic")       
        profile.contact = request.POST.get("contact")       
        profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
        profile.save()
        messages.success(request, "Profile updated successfully!")

    if request.htmx:
        return render(request, "users/components/profileComponent.html", context)
    else:
        return render(request, "users/profile.html", context)

@login_required
def address(request):
    address = Address.objects.get(user=request.user)
    if request.method == "POST":
        address.country = request.POST.get("country")
        address.city = request.POST.get("city")
        address.town_or_area = request.POST.get("town_or_area")
        address.address = request.POST.get("address")
        address.save()
        messages.success(request, "Address updated successfully!")
    context = {
        "address": address,
    }
    if request.htmx:
        return render(request, "users/components/addressComponent.html", context)
    else:
        return render(request, "users/address.html", context)
@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user
        is_password_match = check_password(password, user.password)

        if is_password_match:
            user.delete()
            return redirect("account_login")
        else:
            return HttpResponse("Wrong Password")
    return render(request, "users/delete_account.html")

# def license_ocr(image):
#     # Specify language(s) based on your text content
#     reader = Reader(['ch_sim', 'en'], gpu=False)
#     # Read text from the image
#     result = reader.readtext(image, detail=0)
#     # Combine lines for better string parsing
#     parsed_text = " ".join(result)
#     # Define dictionary to store extracted values
#     extracted_data = {}
#     # Regular expressions for more robust extraction (adapt as needed)
#     name_regex = r"Name\s+([\w ]+)"
#     expiry_regex = r"Expiry Date\s+([\d\-]+)"
#     # Extract values using regular expressions
#     name_match = re.search(name_regex, parsed_text)
#     expiry_match = re.search(expiry_regex, parsed_text)
#     if name_match:
#         extracted_data["name"] = name_match.group(1) or None
#     if expiry_match:
#         extracted_data["expiry_date"] = expiry_match.group(1) or None
#     # Print extracted values for verification
#     name = extracted_data.get('name', None)
#     expiry_date = extracted_data.get('expiry_date', None)
#     return {'name': name, 'expiry_date': expiry_date}

@login_required
def license_info(request):
    license = LicenseDetail.objects.get(user=request.user)
    context = {
        "license": license,
    }
    if request.htmx:
        return render(request, "users/components/licenseComponent.html", context)
    else:
        return render(request, "users/license.html", context)

# HTMX Views:
@login_required
def password_check_for_account_deletion(request):
    enable_button = """ <div class="flex flex-shrink-0 flex-wrap items-center justify-end rounded-b-md p-4">
            <button type="submit" class="ml-2 btn bg-[red]" data-te-ripple-init data-te-ripple-color="light">Delete Account</button>
          </div> """
    disable_button = """ <p class="text-red font-medium">Password don't match.</p>
    <div class="flex flex-shrink-0 flex-wrap items-center justify-end rounded-b-md p-4">
            <button type="submit" class="ml-2 btn bg-[red]" data-te-ripple-init data-te-ripple-color="light" disabled>Delete Account</button>
          </div> """
    password = request.POST.get("password")
    user = request.user
    is_password_match = check_password(password, user.password)

    if is_password_match:
        # Password is correct
        return HttpResponse(enable_button)
    else:
        # Password is incorrect
        return HttpResponse(disable_button)

# @login_required
# def license_image_data_generator(request):
#     name_error = None
#     date_error = None
#     name = None
#     date = None
#     expiry_date = None
#     license = LicenseDetail.objects.get(user = request.user)
#     license.license_pic = request.FILES.get("image") or license.license_pic
#     license.save()
#     extracted_data = license_ocr(license.license_pic.path)
#     name = extracted_data.get('name', None)
#     if not name:
#         name_error = "System couldn't find name. Please use another picture."
#     expiry_date = extracted_data.get('expiry_date', None)
#     if not expiry_date:
#         date_error = "System couldn't find expiry date. Please use another picture."
#     elif expiry_date:
#         # print(f"name: {name}, expiry date: {expiry_date}")
#         date = datetime.strptime(expiry_date, "%d-%m-%Y").date()
#         # print("\n" , date)
#         current_date = timezone.now().date()
#         if date < current_date:
#             date_error = "Your provided License is expired"
#     context = {
#         "name_error": name_error,
#         "date_error": date_error,
#         "name": name,
#         "date": date,
#         "license": license,
#     }
#     return render(request, "users/smallComponents/licenseComponent.html", context)
    # print(license.license_pic.url)
    # license.save()
    # return HttpResponse("done")

@login_required
def manual_license_set(request):
    license = LicenseDetail.objects.get(user = request.user)
    context = {
        "license": license,
    }
    return render(request, "users/smallComponents/manualLicenseComponent.html", context)

@login_required
def license_set_form(request):
    license = LicenseDetail.objects.get(user = request.user)
    if request.method == "POST":
        if "image" in request.POST:
            license.license_pic = request.FILES.get("image") or license.license_pic
        license.license_name = request.POST.get("license_name")
        license.expiry_date = request.POST.get("expiry_date")
        license.valid = True
        license.save()
        return redirect("license_info")
    
def notifications(request):
    notifications = Notification.objects.filter(user = request.user).order_by("-id")
    for notification in notifications:
        if notification.seen == False:
            notification.seen = True
            notification.save()
    context = {
        "notifications": notifications,
    }
    return render(request, "users/smallComponents/notificationComponent.html", context)