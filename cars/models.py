from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator 
from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary.models import CloudinaryField

class Brand(models.Model):
    name = models.CharField(max_length=100, unique = True)
    logo = models.ImageField(upload_to='Brands/logo', null=True)
    description = models.TextField()
    class Meta:
        verbose_name_plural = "Brands"

    def logo_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.logo.url))
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    logo = CloudinaryField('image', public_id='Categories/logo', null=True)
    description = models.TextField()
    class Meta:
        verbose_name_plural = "Categories"

    def logo_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.logo.url))
    def __str__(self):
        return self.name

class Transmission(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Transmissions"
    def __str__(self):
        return self.name

class Fuel_Type(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Fuel Types"
    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100, null=True)
    year_of_manufacture = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(3000)], null=True)
    image = models.ImageField(upload_to='Car/images', null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name = "cars")
    color = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = RichTextUploadingField(null=True, blank=True, default="This is the description")
    per_day_rent = models.PositiveIntegerField()
    weekly_rent = models.PositiveIntegerField(default = 0)
    monthly_rent = models.PositiveIntegerField(default = 0)
    no_of_times_rented = models.PositiveIntegerField(default = 0)
    rented = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Cars"

    def car_image(self):
        return mark_safe('<img src="%s" width="75" height="50"/>'% (self.image.url))
    def security_charges(self):
        self.charges = int(self.per_day_rent * 0.8)
        return self.charges
    def __str__(self):
        return self.name
    
class CarImages(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name = 'images')
    def upload_to(instance):
        return f'DaisyRoom/Car/All_Images/{instance.car.name}_{instance.car.model}_{instance.car.id}/'
    image = CloudinaryField('image', public_id=upload_to, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Car Images"

class Specification(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='specifications')
    max_speed_in_km_per_h = models.IntegerField(validators = [(MinValueValidator(0))], null=True)
    engine_size = models.DecimalField(max_digits=5, decimal_places=2)
    seats = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(100)])
    condition = models.DecimalField(max_digits=5, decimal_places=2, validators = [MinValueValidator(4.00), MaxValueValidator(10.00)])
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(Fuel_Type, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Specifications"
    def car_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.car.image.url))
    def __str__(self):
        return self.car.name

class Features(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='features')
    Air_Conditioner = models.BooleanField(default = False)
    Digital_Odometer = models.BooleanField(default = False)
    Heater = models.BooleanField(default = False)
    Leather_Seats = models.BooleanField(default = False)
    Panoramic_Moonroof = models.BooleanField(default = False)
    Tachometer = models.BooleanField(default = False)
    Touchscreen_Display = models.BooleanField(default = False)
    Antilock_Braking = models.BooleanField(default = False)
    Brake_Assist = models.BooleanField(default = False)
    Child_Safety_Locks = models.BooleanField(default = False)
    Driver_Air_Bag = models.BooleanField(default = False)
    Power_Door_Locks = models.BooleanField(default = False)
    Stability_Control = models.BooleanField(default = False)
    Traction_Control = models.BooleanField(default = False)
    Fog_Lights_Front = models.BooleanField(default = False)
    Rain_Sensing_Wiper = models.BooleanField(default = False)
    Rear_Spoiler = models.BooleanField(default = False)
    Windows_Electric = models.BooleanField(default = False)
    Android_Auto = models.BooleanField(default = False)
    Bluetooth = models.BooleanField(default = False)
    HomeLink = models.BooleanField(default = False)
    Power_Steering = models.BooleanField(default = False)
    class Meta:
        verbose_name_plural = "Features"
    def car_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.car.image.url))
    def __str__(self):
        return self.car.name
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name = "reviews")
    rating = models.IntegerField(choices=[(1, "★☆☆☆☆"),(2, "★★☆☆☆"),(3, "★★★☆☆"),(4, "★★★★☆"),(5, "★★★★★"),])
    review = models.TextField()
    image = models.ImageField(upload_to='Reviews/images', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Reviews"
    def car_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.car.image.url))
    def __str__(self):
        return self.user.username

