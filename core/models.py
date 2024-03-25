from django.db import models

class Customization(models.Model):
    title = models.CharField(max_length=220, default="Customizations", editable=False)
    main_small_heading = models.CharField(max_length=220, default="Find Cars For Rent Near You")
    main_large_heading = models.CharField(max_length=220, default="Rent Your Dream Car")
    main_screen_image_desktop = models.ImageField(upload_to="Images/Main_Images_Desktop", null=True)
    main_screen_image_mobile = models.ImageField(upload_to="Images/Main_Images_Mobile", null=True)
    listing_image_desktop = models.ImageField(upload_to="Images/Listing_Images_desktop", null=True)
    listing_image_mobile = models.ImageField(upload_to="Images/Listing_Images_mobile", null=True)
    class Meta:
        verbose_name_plural = "Customizations"
    def __str__(self):
        return self.title
    
