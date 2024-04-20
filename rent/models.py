from django.db import models
from userauths.models import User  # Import User model from userauths app
from users.models import Notification  # Import Notification model from users app
from cars.models import Car, Specification  # Import Car and Specification models from cars app
from shortuuid.django_fields import ShortUUIDField  # Import ShortUUIDField from shortuuid module
from datetime import timedelta, date  # Import necessary datetime functions
from django.db.models.signals import post_save  # Import post_save signal
from django.dispatch import receiver  # Import receiver decorator
from django.conf import settings  # Import settings module
from django.core.mail import EmailMultiAlternatives  # Import EmailMultiAlternatives for sending emails
from django.template.loader import render_to_string  # Import render_to_string for rendering templates
from django.utils.html import strip_tags  # Import strip_tags to strip HTML tags from email content
from decimal import Decimal  # Import Decimal for precise arithmetic calculations
from dateutil.relativedelta import relativedelta  # Import relativedelta for calculating extended dates

class Rent(models.Model):
    # Define Rent model with required fields
    rid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="12345")  # ShortUUIDField for unique rental ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rents")  # User who rented the car
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="rent")  # Car being rented
    cancelled = models.BooleanField(default=False)  # Flag to indicate if the rental is cancelled
    is_deleted = models.BooleanField(default=False)  # Flag to indicate if the rental is deleted
    delivery_method = models.CharField(max_length=50, choices=[("Pickup", "Pickup"), ("Home Delivery", "Home Delivery")], null=True, blank=True)  # Method of car delivery
    paid = models.BooleanField(default=False)  # Flag to indicate if the rent is paid
    period = models.CharField(max_length=50, choices=[("Day", "Day"), ("Week", "Week"), ("Month", "Month")], null=True, blank=True)  # Duration of rent
    number_of_period = models.PositiveIntegerField(null=True, blank=True)  # Number of periods (days, weeks, or months)
    rent = models.PositiveIntegerField(null=True, blank=True)  # Rent amount
    total_rent = models.PositiveIntegerField(null=True, blank=True)  # Total rent amount including extensions
    is_extended = models.BooleanField(default=False)  # Flag to indicate if the rent is extended
    extended_rent = models.PositiveIntegerField(default=0, null=True, blank=True)  # Additional rent due to extension
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Date and time of creation

    class Meta:
        verbose_name_plural = "Rents"  # Plural name for the model in the admin panel

    def __str__(self):
        return self.rid  # String representation of the rent object

class Extended_Rent(models.Model):
    # Define Extended_Rent model with required fields
    erid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="6789", null=True)  # ShortUUIDField for unique extended rent ID
    rent = models.OneToOneField(Rent, on_delete=models.CASCADE, related_name="extended")  # Rent being extended
    period = models.CharField(max_length=50, choices=[("Day", "Day"), ("Week", "Week"), ("Month", "Month")], null=True, blank=True)  # Duration of extension
    number_of_period = models.PositiveIntegerField(null=True, blank=True)  # Number of periods (days, weeks, or months)
    confirmed = models.BooleanField(default=False)  # Flag to indicate if the extension is confirmed
    extended_at = models.DateTimeField(auto_now_add=True, null=True)  # Date and time of extension

    class Meta:
        verbose_name_plural = "Extended Rents"  # Plural name for the model in the admin panel

    def __str__(self):
        return self.rent.rid  # String representation of the extended rent object

    def extended_date(self):
        # Calculate the extended date based on the extension period and number of periods
        if self.period == "Day":
            delta = timedelta(days=self.number_of_period)
        elif self.period == "Week":
            delta = timedelta(weeks=self.number_of_period)
        elif self.period == "Month":
            delta = timedelta(days=int(30 * self.number_of_period))
        return delta  # Return the extended date as timedelta

    def save(self, *args, **kwargs):
        # Override the save method to handle extension confirmation
        if self.pk:  # Check if the instance is already saved (updating)
            original_instance = Extended_Rent.objects.get(pk=self.pk)
            if self.confirmed != original_instance.confirmed:
                if self.confirmed == True and original_instance.confirmed == False:
                    # Update rent details and notify the user on extension confirmation
                    rent = Rent.objects.get(rid=self.rent.rid)
                    rent.is_extended = True
                    if self.period == "Day":
                        rent.extended_rent = rent.car.per_day_rent * self.number_of_period
                    elif self.period == "Week":
                        rent.extended_rent = rent.car.weekly_rent * self.number_of_period
                    else:
                        rent.extended_rent = rent.car.monthly_rent * self.number_of_period
                    rent.total_rent += rent.extended_rent
                    rent.save()
                    Notification.objects.create(
                        user=self.rent.user,
                        subject="Your rent was Extended.",
                        body=f"Your rent of car '{self.rent.car.name}' was extended by {self.number_of_period} {self.period}."
                    )
                    # Send email notification to the user
                    subject = 'Your car rent was extended successfully.'
                    template_name = 'rent/mail/extended.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid=self.rent.rid)
                    last_date = rent.last_date()
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                    }
                    html_content = render_to_string(template_name, context)
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
        super().save(*args, **kwargs)  # Call the original save method

class Rented_Car(models.Model):
    # Define Rented_Car model with required fields
    rent = models.OneToOneField(Rent, on_delete=models.CASCADE, related_name="rented")  # Rent associated with the rented car
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Date and time of creation
    return_status = models.CharField(
        max_length=50,
        choices=[
            ("Returned", "Returned"),
            ("In Hand", "In Hand"),
            ("Over Dued", "Over Dued"),
            ("To be delivered", "To be delivered"),
            ("To be Picked", "To be Picked"),
            ("Finished", "Finished")
        ],
        null=True,
        blank=True
    )  # Status of car return
    over_due_charges = models.PositiveIntegerField(default=0)  # Charges due to overdue

    class Meta:
        verbose_name_plural = "Rented Cars"  # Plural name for the model in the admin panel

    def last_date(self):
        # Calculate the last date of the rent period including extensions
        extended_time = timedelta(days=0)
        if Extended_Rent.objects.filter(rent=self.rent).exists():
            extended_rent = Extended_Rent.objects.get(rent=self.rent)
            extended_time = extended_rent.extended_date()
        if self.rent.period == "Day":
            delta = timedelta(days=self.rent.number_of_period) + timedelta(hours=10)
        elif self.rent.period == "Week":
            delta = timedelta(weeks=self.rent.number_of_period) + timedelta(hours=10)
        elif self.rent.period == "Month":
            delta = timedelta(days=int(30 * self.rent.number_of_period)) + timedelta(hours=10)
        return self.created_at + delta + extended_time  # Return the last date including extensions

    def over_due(self):
        # Check if the rent is overdue based on the last date
        last_date = self.last_date()
        current_date = date.today()
        return current_date > last_date.date()  # Return True if overdue, False otherwise

    def save(self, *args, **kwargs):
        # Override the save method to handle return status changes
        if self.pk:  # Check if the instance is already saved (updating)
            original_instance = Rented_Car.objects.get(pk=self.pk)
            if self.return_status != original_instance.return_status:
                if self.return_status == "In Hand" and original_instance.return_status == "To be delivered":
                    # Notify the user on successful delivery of the car
                    subject = 'Your Car was delivered Successfully.'
                    template_name = 'rent/mail/delivered.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid=self.rent.rid)
                    last_date = self.last_date()
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                    }
                    html_content = render_to_string(template_name, context)
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
                    Notification.objects.create(
                        user=self.rent.user,
                        subject="Your Car was delivered",
                        body=f"Your rented car '{self.rent.car.name}' was delivered to your doorstep successfully bu our end."
                    )
                # Handle other return status changes similarly
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.rent.rid  # String representation of the rented car object

@receiver(post_save, sender=Rented_Car)
def send_order_mail(sender, instance, created, *args, **kwargs):
    # Send email notification on successful rental payment
    if created:
        subject = 'Your Rental Payment is Successfully Completed.'
        template_name = 'rent/order_success_mail.html'  # Replace with the actual template name
        rent = Rent.objects.get(rid=instance.rent.rid)
        last_date = instance.last_date()
        car = Car.objects.get(id=rent.car.id)
        car.rented = True
        car.save()
        context = {
            'rent': rent,
            "last_date": last_date,
        }
        html_content = render_to_string(template_name, context)
        email = EmailMultiAlternatives(
            subject,
            strip_tags(html_content),
            settings.DEFAULT_FROM_EMAIL,
            [instance.rent.user.email],
        )
        email.content_subtype = 'html'
        email.body = html_content
        email.send()

@receiver(post_save, sender=Extended_Rent)
def send_order_mail(sender, instance, created, *args, **kwargs):
    # Handle extension confirmation and update rent details accordingly
    if created:
        if instance.confirmed == True:
            rent = Rent.objects.get(rid=instance.rent.rid)
            rent.is_extended = True
            if instance.period == "Day":
                rent.extended_rent = rent.car.per_day_rent * instance.number_of_period
            elif instance.period == "Week":
                rent.extended_rent = rent.car.weekly_rent * instance.number_of_period
            else:
                rent.extended_rent = rent.car.monthly_rent * instance.number_of_period
            rent.total_rent += rent.extended_rent
            rent.save()
