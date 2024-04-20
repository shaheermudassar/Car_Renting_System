# Importing necessary modules and classes from Django
from django.shortcuts import render, redirect
# Importing the User model from the userauths app
from userauths.models import User
# Importing models from the users app
from users.models import UserProfile, Address, LicenseDetail, Notification
# Importing models from the cars app
from cars.models import Review, Car
# Importing classes for HTTP responses from Django
from django.http import HttpResponse, HttpResponseRedirect
# Importing a decorator to require login for accessing views
from django.contrib.auth.decorators import login_required
# Importing a function to check passwords
from django.contrib.auth.hashers import check_password
# Importing necessary modules for working with dates and times
from datetime import datetime
from django.utils import timezone
# Importing models from the rent app
from rent.models import Rent, Rented_Car
# Importing necessary modules for displaying messages
from django.contrib import messages
from rent.models import Extended_Rent
# from easyocr import Reader
# import re, os

# Decorator to specify that the user must be logged in to access the view
@login_required
def user(request):
    # Getting the URL name from the current request
    url_name = request.resolver_match.url_name
    # Checking if it's an HTMX request and if the URL name is 'full_dashboard'
    if request.htmx and url_name == 'full_dashboard':
        # Rendering a specific template for the full dashboard
        return render(request, "users/components/fulldashboardComponent.html")
    # If it's an HTMX request but not for the full dashboard
    elif request.htmx:
        # Rendering a template for the user component
        return render(request, "users/components/userComponent.html")
    else:
        # Rendering the default user template
        return render(request, "users/user.html")

# Decorator to specify that the user must be logged in to access the view
@login_required
def dashboard(request):
    # Querying rented cars associated with the current user and ordering them by id in descending order
    rents = Rented_Car.objects.filter(rent__user=request.user).order_by("-id")
    # Creating a context dictionary with the rents data
    context = {
        "rents": rents,
    }
    # Checking if it's an HTMX request
    if request.htmx:
        # Rendering a specific template for the dashboard component with the context data
        return render(request, "users/components/dashboardComponent.html", context)
    else:
        # Rendering the default dashboard template with the context data
        return render(request, "users/dashboard.html", context)

# Decorator to specify that the user must be logged in to access the view
@login_required
def rent_detail(request, rid):
    # Initializing variables to track whether the rent has been reviewed and if it's extended
    reviewed = False
    extended_rent = False
    
    # Retrieving the rent object using the provided rent ID (rid)
    rent = Rent.objects.get(rid=rid)
    
    # Checking if there is an extended rent associated with the current rent
    if Extended_Rent.objects.filter(rent=rent).exists():
        # Setting extended_rent to True if an extended rent exists
        extended_rent = True
    
    # Retrieving the car associated with the rent
    car_id = rent.car.id
    car = Car.objects.get(id=car_id)
    
    # Checking if the current user has already reviewed the car
    if Review.objects.filter(user=request.user, car=car).exists():
        # Setting reviewed to True if a review exists for the current user and car
        reviewed = True
    
    # Creating a context dictionary with the rent, reviewed, and extended_rent data
    context = {
        "rent": rent,
        "reviewed": reviewed,
        "extended_rent": extended_rent,
    }
    
    # Checking if it's an HTMX request
    if request.htmx:
        # Rendering a specific template for the rent detail component with the context data
        return render(request, "users/components/rent_detailComponent.html", context)
    else:
        # Rendering the default rent detail template with the context data
        return render(request, "users/rent_detail.html", context)

# Decorator to specify that the user must be logged in to access the view
@login_required
def profile(request):
    # Retrieving the user's profile object based on the logged-in user
    profile = UserProfile.objects.get(user=request.user)
    
    # Creating a context dictionary with the profile object
    context = {
        "profile": profile,
    }
    
    # Checking if the request method is POST, meaning the user is updating their profile
    if request.method == 'POST':
        # Updating the profile fields with the data from the POST request
        profile.first_name = request.POST.get("first_name")
        profile.last_name = request.POST.get("last_name")
        profile.cnic = request.POST.get("cnic")
        profile.contact = request.POST.get("contact")
        profile.profile_pic = request.FILES.get("profile_pic") or profile.profile_pic
        
        # Saving the updated profile object
        profile.save()
        
        # Displaying a success message after profile update
        messages.success(request, "Profile updated successfully!")
    
    # Checking if it's an HTMX request
    if request.htmx:
        # Rendering a specific template for the profile component with the context data
        return render(request, "users/components/profileComponent.html", context)
    else:
        # Rendering the default profile template with the context data
        return render(request, "users/profile.html", context)

# Decorator to specify that the user must be logged in to access the view
@login_required
def address(request):
    # Retrieving the user's address object based on the logged-in user
    address = Address.objects.get(user=request.user)
    
    # Checking if the request method is POST, meaning the user is updating their address
    if request.method == "POST":
        # Updating the address fields with the data from the POST request
        address.country = request.POST.get("country")
        address.city = request.POST.get("city")
        address.town_or_area = request.POST.get("town_or_area")
        address.address = request.POST.get("address")
        
        # Saving the updated address object
        address.save()
        
        # Displaying a success message after address update
        messages.success(request, "Address updated successfully!")
    
    # Creating a context dictionary with the address object
    context = {
        "address": address,
    }
    
    # Checking if it's an HTMX request
    if request.htmx:
        # Rendering a specific template for the address component with the context data
        return render(request, "users/components/addressComponent.html", context)
    else:
        # Rendering the default address template with the context data
        return render(request, "users/address.html", context)

# Decorator to specify that the user must be logged in to access the view
@login_required
def delete_account(request):
    # Checking if the request method is POST, meaning the user is trying to delete their account
    if request.method == "POST":
        # Retrieving the password from the POST request
        password = request.POST.get("password")
        user = request.user
        
        # Checking if the entered password matches the user's password
        is_password_match = check_password(password, user.password)
        
        # If password matches, delete the user's account and redirect to login page
        if is_password_match:
            user.delete()
            return redirect("account_login")
        # If password doesn't match, return an error message
        else:
            return HttpResponse("Wrong Password")
    
    # Rendering the delete account page
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
# Decorator to specify that the user must be logged in to access the view
@login_required
def license_info(request):
    # Retrieving the license details of the logged-in user
    license = LicenseDetail.objects.get(user=request.user)
    
    # Creating a context dictionary with the license details
    context = {
        "license": license,
    }
    
    # Checking if it's an HTMX request
    if request.htmx:
        # Rendering a specific template for the license component with the context data
        return render(request, "users/components/licenseComponent.html", context)
    else:
        # Rendering the default license template with the context data
        return render(request, "users/license.html", context)

# HTMX Views:

# View to check the password for account deletion using HTMX
@login_required
def password_check_for_account_deletion(request):
    # HTML code for the button when password matches
    enable_button = """ <div class="flex flex-shrink-0 flex-wrap items-center justify-end rounded-b-md p-4">
            <button type="submit" class="ml-2 btn bg-[red]" data-te-ripple-init data-te-ripple-color="light">Delete Account</button>
          </div> """
    
    # HTML code for the button when password does not match
    disable_button = """ <p class="text-red font-medium">Password don't match.</p>
    <div class="flex flex-shrink-0 flex-wrap items-center justify-end rounded-b-md p-4">
            <button type="submit" class="ml-2 btn bg-[red]" data-te-ripple-init data-te-ripple-color="light" disabled>Delete Account</button>
          </div> """
    
    # Retrieving the password from the POST request
    password = request.POST.get("password")
    user = request.user
    
    # Checking if the entered password matches the user's password
    is_password_match = check_password(password, user.password)

    # If password matches, return the HTML code for enabling the delete account button
    if is_password_match:
        return HttpResponse(enable_button)
    # If password doesn't match, return the HTML code for disabling the delete account button
    else:
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
# View to manually set license details
@login_required
def manual_license_set(request):
    # Retrieving the license details of the logged-in user
    license = LicenseDetail.objects.get(user=request.user)
    
    # Creating a context dictionary with the license details
    context = {
        "license": license,
    }
    
    # Rendering the manual license setting form with the context data
    return render(request, "users/smallComponents/manualLicenseComponent.html", context)

# View to handle the license setting form submission
@login_required
def license_set_form(request):
    # Retrieving the license details of the logged-in user
    license = LicenseDetail.objects.get(user=request.user)
    
    # Handling the POST request for updating license details
    if request.method == "POST":
        # Checking if the image field is present in the form data
        if "image" in request.POST:
            # Updating the license picture field with the uploaded image or keeping the existing one
            license.license_pic = request.FILES.get("image") or license.license_pic
        # Updating other license details based on form input
        license.license_name = request.POST.get("license_name")
        license.expiry_date = request.POST.get("expiry_date")
        license.valid = True
        license.save()
        # Redirecting to the license information page after successful update
        return redirect("license_info")

# View to display notifications
def notifications(request):
    # Retrieving notifications for the logged-in user and ordering them by ID
    notifications = Notification.objects.filter(user=request.user).order_by("-id")
    # Marking unseen notifications as seen
    for notification in notifications:
        if notification.seen == False:
            notification.seen = True
            notification.save()
    
    # Creating a context dictionary with the notifications
    context = {
        "notifications": notifications,
    }
    
    # Rendering the notifications component with the context data
    return render(request, "users/smallComponents/notificationComponent.html", context)
