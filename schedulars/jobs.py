from rent.models import Rented_Car, Rent  # Importing necessary models
from users.models import Notification  # Importing Notification model
from datetime import datetime, date  # Importing datetime classes
from django.conf import settings  # Importing project settings
from django.core.mail import EmailMessage  # Importing EmailMessage class for sending emails
from django.template.loader import render_to_string  # Importing render_to_string to render HTML templates
from django.utils.html import strip_tags  # Importing strip_tags to strip HTML tags from email content
from apscheduler.schedulers.background import BackgroundScheduler  # Importing BackgroundScheduler for scheduling jobs

# Function to send overdue emails
def send_overdue_emails():
    overdue_rented_cars = Rented_Car.objects.all()  # Get all rented cars
    current_date = datetime.now().replace(tzinfo=None)  # Get current date and time
    for rented_car in overdue_rented_cars:
        if (rented_car.last_date().replace(tzinfo=None) < current_date and (rented_car.return_status == "In Hand" or rented_car.return_status == "Over Dued")):
            if rented_car.return_status == "In Hand":
                rented_car.return_status = "Over Dued"
                rented_car.save()
            subject = 'Please return your rented car to our garage.'  # Email subject
            template_name = 'rent/mail/overdued.html'  # Template for the email
            rent = Rent.objects.get(rid=rented_car.rent.rid)  # Get rent associated with the rented car
            last_date = rented_car.last_date()  # Get the last date of the rent
            context = {  # Context data for the email template
                'rent': rent,
                "last_date": last_date,
            }
            html_content = render_to_string(template_name, context)  # Render HTML content from the template
            email = EmailMessage(  # Create an EmailMessage object
                subject,
                strip_tags(html_content),  # Plain text version of the HTML content
                settings.DEFAULT_FROM_EMAIL,
                [rented_car.rent.user.email],  # Recipient email address
            )
            email.content_subtype = 'html'  # Set content type to HTML
            email.body = html_content  # Set email body
            email.send()  # Send the email
            overdue_charges_to_be_added = rented_car.rent.car.per_day_rent  # Calculate overdue charges
            rented_car.over_due_charges += overdue_charges_to_be_added  # Add overdue charges to rented car
            rented_car.save()  # Save the rented car
            Notification.objects.create(  # Create a notification for the user
                user=rented_car.rent.user,
                subject='Please return your rented car to our garage.',
                body=f"You haven't returned your rented car '{rent.car.name}' to our garage yet."
            )

# Function to send reminders and finish rents on the last date
def last_date_reminder_and_rent_finisher_aps():
    current_date = date.today()  # Get current date
    rented_cars = Rented_Car.objects.all()  # Get all rented cars
    filtered_rents = [rent for rent in rented_cars if rent.last_date().date() == current_date]  # Filter rents with last date equal to current date

    for rented_car in filtered_rents:
        if rented_car.return_status == "In Hand":
            subject = 'Reminder! Today is the last date to return your car.'  # Email subject
            template_name = 'rent/mail/last_date.html'  # Template for the email
            rent = Rent.objects.get(rid=rented_car.rent.rid)  # Get rent associated with the rented car
            last_date = rented_car.last_date()  # Get the last date of the rent
            context = {  # Context data for the email template
                'rent': rent,
                "last_date": last_date,
            }
            html_content = render_to_string(template_name, context)  # Render HTML content from the template
            email = EmailMessage(  # Create an EmailMessage object
                subject,
                strip_tags(html_content),  # Plain text version of the HTML content
                settings.DEFAULT_FROM_EMAIL,
                [rented_car.rent.user.email],  # Recipient email address
            )
            email.content_subtype = 'html'  # Set content type to HTML
            email.body = html_content  # Set email body
            email.send()  # Send the email
            Notification.objects.create(  # Create a notification for the user
                user=rented_car.rent.user,
                subject='Reminder! Last date of return.',
                body=f"Today is the last date to return your rented car '{rent.car.name}' to our garage."
            )
        elif rented_car.return_status == "To be Picked":
            rented_car.return_status = "Finished"  # Set return status to Finished
            rented_car.save()  # Save the rented car
            subject = 'Car Rent Finished!'  # Email subject
            template_name = 'rent/mail/finished_before_pick.html'  # Template for the email
            rent = Rent.objects.get(rid=rented_car.rent.rid)  # Get rent associated with the rented car
            last_date = rented_car.last_date()  # Get the last date of the rent
            context = {  # Context data for the email template
                'rent': rent,
                "last_date": last_date,
            }
            html_content = render_to_string(template_name, context)  # Render HTML content from the template
            email = EmailMessage(  # Create an EmailMessage object
                subject,
                strip_tags(html_content),  # Plain text version of the HTML content
                settings.DEFAULT_FROM_EMAIL,
                [rented_car.rent.user.email],  # Recipient email address
            )
            email.content_subtype = 'html'  # Set content type to HTML
            email.body = html_content  # Set email body
            email.send()  # Send the email
            Notification.objects.create(  # Create a notification for the user
                user=rented_car.rent.user,
                subject='Car Rent Finished!',
                body=f"You didn't pick your rented car '{rent.car.name}' from our garage till the last date, so the rent was finished."
            )