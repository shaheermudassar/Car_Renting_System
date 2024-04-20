from rent.models import Rented_Car, Rent
from users.models import Notification
from datetime import datetime, date
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_overdue_emails():
    overdue_rented_cars = Rented_Car.objects.all()
    current_date = datetime.now().replace(tzinfo=None)
    for rented_car in overdue_rented_cars:
        if (rented_car.last_date().replace(tzinfo=None) < current_date and (rented_car.return_status == "In Hand" or rented_car.return_status == "Over Dued")):
            if rented_car.return_status == "In Hand":
                rented_car.return_status = "Over Dued"
                rented_car.save()
            subject = 'Please return your rented car to our garage.'
            template_name = 'rent/mail/overdued.html'  # Replace with the actual template name
            rent = Rent.objects.get(rid = rented_car.rent.rid)
            last_date = rented_car.last_date()
            # Your context data
            context = {
                'rent': rent,
                "last_date": last_date,
                # Add more variables as needed
                }
            # Render the HTML content from a template using the provided context
            html_content = render_to_string(template_name, context)
            # Create an EmailMessage object
            email = EmailMessage(
                subject,
                strip_tags(html_content),  # Plain text version of the HTML content
                settings.DEFAULT_FROM_EMAIL,
                [rented_car.rent.user.email],
            )
            # Attach the HTML content
            email.content_subtype = 'html'
            email.body = html_content
            email.send()
            overdue_charges_to_be_added = rented_car.rent.car.per_day_rent
            rented_car.over_due_charges += overdue_charges_to_be_added
            rented_car.save()
            print("mailed")
            Notification.objects.create(
                user = rented_car.rent.user,
                subject = 'Please return your rented car to our garage.',
                body = f"You haven't returned your rented car '{rent.car.name}' to our garage yet."
            )
    print("\n")

def last_date_reminder_and_rent_finisher_aps():
    current_date = date.today()
    rented_cars = Rented_Car.objects.all()
    filtered_rents = [rent for rent in rented_cars if rent.last_date().date() == current_date]

    for rented_car in filtered_rents:
        if rented_car.return_status == "In Hand":
            subject = 'Reminder! Today is last date to return your car.'
            template_name = 'rent/mail/last_date.html'  # Replace with the actual template name
            rent = Rent.objects.get(rid = rented_car.rent.rid)
            last_date = rented_car.last_date()
            # Your context data
            context = {
                'rent': rent,
                "last_date": last_date,
                # Add more variables as needed
                }
            # Render the HTML content from a template using the provided context
            html_content = render_to_string(template_name, context)
            # Create an EmailMessage object
            email = EmailMessage(
                subject,
                strip_tags(html_content),  # Plain text version of the HTML content
                settings.DEFAULT_FROM_EMAIL,
                [rented_car.rent.user.email],
            )
            # Attach the HTML content
            email.content_subtype = 'html'
            email.body = html_content
            email.send()
            print("mailed")
            Notification.objects.create(
                user = rented_car.rent.user,
                subject = 'Reminder! last date of return.',
                body = f"Today is the last date to return your rented car '{rent.car.name}' to our garage."
            )
        elif rented_car.return_status == "To be Picked":
            rented_car.return_status = "Finished"
            rented_car.save()
            subject = 'Car Rent Finished!'
            template_name = 'rent/mail/finished_before_pick.html'  # Replace with the actual template name
            rent = Rent.objects.get(rid = rented_car.rent.rid)
            last_date = rented_car.last_date()
            # Your context data
            context = {
                'rent': rent,
                "last_date": last_date,
                # Add more variables as needed
                }
            # Render the HTML content from a template using the provided context
            html_content = render_to_string(template_name, context)
            # Create an EmailMessage object
            email = EmailMessage(
                subject,
                strip_tags(html_content),  # Plain text version of the HTML content
                settings.DEFAULT_FROM_EMAIL,
                [rented_car.rent.user.email],
            )
            # Attach the HTML content
            email.content_subtype = 'html'
            email.body = html_content
            email.send()
            print("mailed")
            Notification.objects.create(
                user = rented_car.rent.user,
                subject = 'Car Rent Finished!',
                body = f"You didn't picked your rented car '{rent.car.name}' from our garage till last date so rent was finished."
            )
    print("\n")