# Importing required modules from Django
from django.db import models  # Module for defining database models
from userauths.models import User  # Importing the User model from userauths app
from django.utils.html import mark_safe  # Module for generating safe HTML content
from django.core.validators import MaxValueValidator, MinValueValidator  # Module for defining validators
from ckeditor_uploader.fields import RichTextUploadingField  # Field for rich text content with CKEditor
from cloudinary.models import CloudinaryField  # Field for handling Cloudinary uploads

# Defining the Brand model
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the brand
    logo = models.ImageField(upload_to='Brands/logo', null=True)  # Logo image of the brand
    description = models.TextField()  # Description of the brand

    class Meta:
        verbose_name_plural = "Brands"  # Plural name for the model in admin interface

    def logo_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.logo.url))  # Method to display logo as HTML

    def __str__(self):
        return self.name  # String representation of the brand

# Defining the Category model
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    logo = CloudinaryField('image', public_id='Categories/logo', null=True)  # Logo image of the category
    description = models.TextField()  # Description of the category

    class Meta:
        verbose_name_plural = "Categories"  # Plural name for the model in admin interface

    def logo_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.logo.url))  # Method to display logo as HTML

    def __str__(self):
        return self.name  # String representation of the category

# Defining the Transmission model
class Transmission(models.Model):
    name = models.CharField(max_length=100)  # Name of the transmission type

    class Meta:
        verbose_name_plural = "Transmissions"  # Plural name for the model in admin interface

    def __str__(self):
        return self.name  # String representation of the transmission type

# Defining the Fuel_Type model
class Fuel_Type(models.Model):
    name = models.CharField(max_length=100)  # Name of the fuel type

    class Meta:
        verbose_name_plural = "Fuel Types"  # Plural name for the model in admin interface

    def __str__(self):
        return self.name  # String representation of the fuel type

# Defining the Car model
class Car(models.Model):
    name = models.CharField(max_length=100)  # Name of the car
    model = models.CharField(max_length=100, null=True)  # Model of the car
    year_of_manufacture = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(3000)], null=True)  # Year of manufacture
    image = models.ImageField(upload_to='Car/images', null=True)  # Image of the car
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="cars")  # Brand of the car
    color = models.CharField(max_length=100)  # Color of the car
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category of the car
    description = RichTextUploadingField(null=True, blank=True, default="This is the description")  # Description of the car
    per_day_rent = models.PositiveIntegerField()  # Rent per day
    weekly_rent = models.PositiveIntegerField(default=0)  # Rent per week
    monthly_rent = models.PositiveIntegerField(default=0)  # Rent per month
    no_of_times_rented = models.PositiveIntegerField(default=0)  # Number of times rented
    rented = models.BooleanField(default=False)  # Rental status
    is_deleted = models.BooleanField(default=False)  # Deletion status
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation

    class Meta:
        verbose_name_plural = "Cars"  # Plural name for the model in admin interface

    def car_image(self):
        return mark_safe('<img src="%s" width="75" height="50"/>' % (self.image.url))  # Method to display car image as HTML

    def security_charges(self):
        self.charges = int(self.per_day_rent * 0.8)  # Method to calculate security charges
        return self.charges

    def __str__(self):
        return self.name  # String representation of the car

# Defining the CarImages model
class CarImages(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')  # Car associated with the image

    def upload_to(instance):
        return f'DaisyRoom/Car/All_Images/{instance.car.name}_{instance.car.model}_{instance.car.id}'  # Method to define upload path

    image = CloudinaryField('image', public_id=upload_to, null=True)  # Image of the car
    added_at = models.DateTimeField(auto_now_add=True)  # Date and time of addition

    class Meta:
        verbose_name_plural = "Car Images"  # Plural name for the model in admin interface

# Defining the Specification model
class Specification(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='specifications')  # Car associated with the specification
    max_speed_in_km_per_h = models.IntegerField(validators=[(MinValueValidator(0))], null=True)  # Maximum speed
    engine_size = models.DecimalField(max_digits=5, decimal_places=2)  # Engine size
    seats = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])  # Number of seats
    condition = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(4.00), MaxValueValidator(10.00)])  # Condition rating
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE)  # Transmission type
    fuel_type = models.ForeignKey(Fuel_Type, on_delete=models.CASCADE)  # Fuel type

    class Meta:
        verbose_name_plural = "Specifications"  # Plural name for the model in admin interface

    def car_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.car.image.url))  # Method to display car image as HTML

    def __str__(self):
        return self.car.name  # String representation of the specification

# Defining the Features model
class Features(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='features')  # Car associated with the features
    # Features
    Air_Conditioner = models.BooleanField(default=False)
    Digital_Odometer = models.BooleanField(default=False)
    Heater = models.BooleanField(default=False)
    Leather_Seats = models.BooleanField(default=False)
    Panoramic_Moonroof = models.BooleanField(default=False)
    Tachometer = models.BooleanField(default=False)
    Touchscreen_Display = models.BooleanField(default=False)
    Antilock_Braking = models.BooleanField(default=False)
    Brake_Assist = models.BooleanField(default=False)
    Child_Safety_Locks = models.BooleanField(default=False)
    Driver_Air_Bag = models.BooleanField(default=False)
    Power_Door_Locks = models.BooleanField(default=False)
    Stability_Control = models.BooleanField(default=False)
    Traction_Control = models.BooleanField(default=False)
    Fog_Lights_Front = models.BooleanField(default=False)
    Rain_Sensing_Wiper = models.BooleanField(default=False)
    Rear_Spoiler = models.BooleanField(default=False)
    Windows_Electric = models.BooleanField(default=False)
    Android_Auto = models.BooleanField(default=False)
    Bluetooth = models.BooleanField(default=False)
    HomeLink = models.BooleanField(default=False)
    Power_Steering = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Features"  # Plural name for the model in admin interface

    def car_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.car.image.url))  # Method to display car image as HTML

    def __str__(self):
        return self.car.name  # String representation of the features

# Defining the Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who posted the review
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reviews")  # Car associated with the review
    rating = models.IntegerField(choices=[(1, "★☆☆☆☆"), (2, "★★☆☆☆"), (3, "★★★☆☆"), (4, "★★★★☆"), (5, "★★★★★"),])  # Rating
    review = models.TextField()  # Review content
    image = models.ImageField(upload_to='Reviews/images', null=True, blank=True)  # Image attached to the review

    class Meta:
        verbose_name_plural = "Reviews"  # Plural name for the model in admin interface

    def car_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.car.image.url))  # Method to display car image as HTML

    def __str__(self):
        return self.user.username  # String representation of the review
