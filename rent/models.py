from django.db import models
from userauths.models import User
from users.models import Notification
from cars.models import Car, Specification
from shortuuid.django_fields import ShortUUIDField
from datetime import timedelta, date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import Decimal
from dateutil.relativedelta import relativedelta

class Rent(models.Model):
    rid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="12345")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "rents")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name = "rent")
    cancelled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    delivery_method = models.CharField(max_length = 50, choices=[("Pickup", "Pickup"),("Home Delivery", "Home Delivery")], null = True, blank = True)
    paid = models.BooleanField(default = False)
    period = models.CharField(max_length = 50, choices=[("Day", "Day"),("Week", "Week"),("Month", "Month")], null = True, blank = True)
    number_of_period = models.PositiveIntegerField(null = True, blank = True)
    rent = models.PositiveIntegerField(null = True, blank = True)
    total_rent = models.PositiveIntegerField(null = True, blank = True)
    is_extended = models.BooleanField(default = False)
    extended_rent = models.PositiveIntegerField(default = 0, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    class Meta:
        verbose_name_plural = "Rents"
    def __str__(self):
        return self.rid

class Extended_Rent(models.Model):
    erid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="6789", null = True)
    rent = models.OneToOneField(Rent, on_delete=models.CASCADE, related_name = "extended")
    period = models.CharField(max_length = 50, choices=[("Day", "Day"),("Week", "Week"),("Month", "Month")], null = True, blank = True)
    number_of_period = models.PositiveIntegerField(null = True, blank = True)
    confirmed = models.BooleanField(default = False)
    extended_at = models.DateTimeField(auto_now_add = True, null = True)
    class Meta:
        verbose_name_plural = "Extended Rents"
    def __str__(self):
        return self.rent.rid
    def extended_date(self):
        if self.period == "Day":
            delta = timedelta(days=self.number_of_period)
        elif self.period == "Week":
            delta = timedelta(weeks=self.number_of_period)
        elif self.period == "Month":
            delta = timedelta(days = int(30 * self.number_of_period))
        return delta
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance is already saved (updating)
            original_instance = Extended_Rent.objects.get(pk=self.pk)
            if self.confirmed != original_instance.confirmed:
                if self.confirmed == True and original_instance.confirmed == False:
                    rent = Rent.objects.get(rid = self.rent.rid)
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
                        user = self.rent.user,
                        subject = "Your rent was Extended.",
                        body = f"Your rent of car '{self.rent.car.name}' was extended by {self.number_of_period} {self.period}."
                    )
                    subject = 'Your car rent was extended successfully.'
                    template_name = 'rent/mail/extended.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid = self.rent.rid)
                    last_date = self.last_date()
                    # Your context data
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                        # Add more variables as needed
                    }
                    # Render the HTML content from a template using the provided context
                    html_content = render_to_string(template_name, context)
                    # Create an EmailMultiAlternatives object
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),  # Plain text version of the HTML content
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    # Attach the HTML content
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
                    print("mailed")
        super().save(*args, **kwargs)

class Rented_Car(models.Model):
    rent = models.OneToOneField(Rent, on_delete=models.CASCADE, related_name = "rented")
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    return_status = models.CharField(
        max_length = 50,
        choices=[
            ("Returned", "Returned"),
            ("In Hand", "In Hand"),
            ("Over Dued", "Over Dued"),
            ("To be delivered", "To be delivered"),
            ("To be Picked", "To be Picked"),
            ("Finished", "Finished")
            ],
        null = True,
        blank = True)
    over_due_charges = models.PositiveIntegerField(default = 0)
    class Meta:
        verbose_name_plural = "Rented Cars"
    def last_date(self):
        extended_time = timedelta(days = 0)
        if Extended_Rent.objects.filter(rent = self.rent).exists():
            extended_rent = Extended_Rent.objects.get(rent = self.rent)
            extended_time = extended_rent.extended_date()
        if self.rent.period == "Day":
            delta = timedelta(days=self.rent.number_of_period) + timedelta(hours=10)
        elif self.rent.period == "Week":
            delta = timedelta(weeks=self.rent.number_of_period) + timedelta(hours=10)
        elif self.rent.period == "Month":
            delta = timedelta(days = int(30 * self.rent.number_of_period)) + timedelta(hours=10)
        return self.created_at + delta + extended_time
    def over_due(self):
        last_date = self.last_date()
        current_date = date.today()
        return current_date > last_date.date()
    def save(self, *args, **kwargs):
        # Check if the return_status has changed
        if self.pk:  # Check if the instance is already saved (updating)
            original_instance = Rented_Car.objects.get(pk=self.pk)
            if self.return_status != original_instance.return_status:
                if self.return_status == "In Hand" and original_instance.return_status == "To be delivered":
                    subject = 'Your Car was delivered Successfully.'
                    template_name = 'rent/mail/delivered.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid = self.rent.rid)
                    last_date = self.last_date()
                    # Your context data
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                        # Add more variables as needed
                    }
                    # Render the HTML content from a template using the provided context
                    html_content = render_to_string(template_name, context)
                    # Create an EmailMultiAlternatives object
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),  # Plain text version of the HTML content
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    # Attach the HTML content
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
                    print("mailed")
                    Notification.objects.create(
                        user = self.rent.user,
                        subject = "Your Car was delivered",
                        body = f"Your rented car '{self.rent.car.name}' was delivered to your doorstep successfully bu our end."
                    )
                elif self.return_status == "In Hand" and original_instance.return_status == "To be Picked":
                    subject = 'Thank You for picking up your car from our Garage.'
                    template_name = 'rent/mail/picked.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid = self.rent.rid)
                    last_date = self.last_date()
                    # Your context data
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                        # Add more variables as needed
                    }
                    # Render the HTML content from a template using the provided context
                    html_content = render_to_string(template_name, context)
                    # Create an EmailMultiAlternatives object
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),  # Plain text version of the HTML content
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    # Attach the HTML content
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
                    print("mailed")
                    Notification.objects.create(
                        user = self.rent.user,
                        subject = "Your Car was picked by you.",
                        body = f"Thank You for picking up your car '{self.rent.car.name}' from our Garage."
                    )
                elif self.return_status == "Returned" and original_instance.return_status == "In Hand":
                    subject = 'Thank You for Returning the car.'
                    template_name = 'rent/mail/returned.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid = self.rent.rid)
                    last_date = self.last_date()
                    
                    # Your context data
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                        # Add more variables as needed
                    }
                    # Render the HTML content from a template using the provided context
                    html_content = render_to_string(template_name, context)
                    # Create an EmailMultiAlternatives object
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),  # Plain text version of the HTML content
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    # Attach the HTML content
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
                    car = Car.objects.get(id = rent.car.id)
                    car.rented = False
                    condition_to_be_reduced = 0.00
                    if rent.period == "Month" and rent.number_of_period > 4:
                        condition_to_be_reduced = 1.00
                    elif rent.period == "Month" and rent.number_of_period < 5:
                        condition_to_be_reduced = 0.5
                    elif rent.period == "Week":
                        condition_to_be_reduced = 0.1
                    elif rent.period == "Day":
                        condition_to_be_reduced = 0.05
                    specification = Specification.objects.get(car = car)
                    specification.condition -= Decimal(str(condition_to_be_reduced))
                    specification.save()
                    car.save()
                    print("mailed")
                    Notification.objects.create(
                        user = self.rent.user,
                        subject = "Your Car was returned.",
                        body = f"Thank You for returning your car '{self.rent.car.name}' back to our Garage."
                    )
                elif self.return_status == "Finished" and original_instance.return_status == "To be Picked":
                    subject = 'Your rent was finished.'
                    template_name = 'rent/mail/finished_before_pick.html'  # Replace with the actual template name
                    rent = Rent.objects.get(rid = self.rent.rid)
                    last_date = self.last_date()
                    
                    # Your context data
                    context = {
                        'rent': rent,
                        "last_date": last_date,
                        # Add more variables as needed
                    }
                    # Render the HTML content from a template using the provided context
                    html_content = render_to_string(template_name, context)
                    # Create an EmailMultiAlternatives object
                    email = EmailMultiAlternatives(
                        subject,
                        strip_tags(html_content),  # Plain text version of the HTML content
                        settings.DEFAULT_FROM_EMAIL,
                        [self.rent.user.email],
                    )
                    # Attach the HTML content
                    email.content_subtype = 'html'
                    email.body = html_content
                    email.send()
                    print("mailed")
                    Notification.objects.create(
                        user = self.rent.user,
                        subject = "Your rent was finished.",
                        body = f"You didn't picked your rented car '{self.rent.car.name}' so we finished your rent."
                    )
        super().save(*args, **kwargs)
    def __str__(self):
        return self.rent.rid
    
@receiver(post_save, sender=Rented_Car)
def send_order_mail(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'Your Rental Payment is Successfully Completed.'
        template_name = 'rent/order_success_mail.html'  # Replace with the actual template name
        rent = Rent.objects.get(rid = instance.rent.rid)
        last_date = instance.last_date()
        car = Car.objects.get(id = rent.car.id)
        car.rented = True
        car.save()
        # Your context data
        context = {
            'rent': rent,
            "last_date": last_date,
            # Add more variables as needed
        }

        # Render the HTML content from a template using the provided context
        html_content = render_to_string(template_name, context)

        # Create an EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            subject,
            strip_tags(html_content),  # Plain text version of the HTML content
            settings.DEFAULT_FROM_EMAIL,
            [instance.rent.user.email],
        )

        # Attach the HTML content
        email.content_subtype = 'html'
        email.body = html_content

        email.send()

@receiver(post_save, sender=Extended_Rent)
def send_order_mail(sender, instance, created, *args, **kwargs):
    if created:
        if instance.confirmed == True:
            rent = Rent.objects.get(rid = instance.rent.rid)
            rent.is_extended = True
            if instance.period == "Day":
                rent.extended_rent = rent.car.per_day_rent * instance.number_of_period
            elif instance.period == "Week":
                rent.extended_rent = rent.car.weekly_rent * instance.number_of_period
            else:
                rent.extended_rent = rent.car.monthly_rent * instance.number_of_period
            rent.total_rent += rent.extended_rent
            rent.save()