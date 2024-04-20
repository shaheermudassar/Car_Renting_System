from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from cars.models import Car

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    cnic = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='Users/Profile_pics', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "User_Profiles"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    def profile_image(self):
        if self.profile_pic:
            return mark_safe('<img src="%s" width="50" height="50"/>'% (self.profile_pic.url))
        else:
            return self.user.username
    
    def __str__(self):
        if self.first_name:
            return self.first_name
        else:
            return self.user.username
    
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "address")
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    town_or_area = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Address"
    def __str__(self):
        return self.user.username

class Saved_Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "saves")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Saved Cars"
    def __str__(self):
        return self.user.username

class LicenseDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "license")
    license_pic = models.ImageField(upload_to='Users/License', null=True, blank=True)
    license_name = models.CharField(max_length=100, null = True, blank = True)
    expiry_date = models.DateField(null = True, blank = True)
    valid = models.BooleanField(default = False)
    class Meta:
        verbose_name_plural = "License Details"
    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "notifications")
    subject = models.CharField(max_length=255, null = True)
    body = models.TextField(null=True)
    seen = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Notifications"
    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        if not UserProfile.objects.filter(user=instance).exists():
            UserProfile.objects.create(
                user=instance,
                first_name = instance.first_name or None, 
                last_name=instance.last_name or None),
        profile = UserProfile.objects.get(user=instance)
        Address.objects.create(user = instance, profile = profile)
        LicenseDetail.objects.create(user = instance)