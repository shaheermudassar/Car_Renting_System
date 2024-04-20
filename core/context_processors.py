from cars.models import Car, Brand, Category
from core.filters import CarFilter
from users.models import UserProfile, Saved_Car
from core.models import Customization
from allauth.socialaccount.models import SocialAccount
def default(request):
    customization = None
    if Customization.objects.filter(title = "Customizations").exists():
        customization = Customization.objects.get(title = "Customizations")
    user = None
    profile_pic = None
    saved_cars = None
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        saved_cars = Saved_Car.objects.filter(user=request.user)
    if request.user.is_authenticated:
        if SocialAccount.objects.filter(user=request.user, provider = "google").exists():
        # if request.user.social.filter(provider='google').exists(): 
            social = SocialAccount.objects.get(user=request.user, provider = "google")
            profile_pic = social.extra_data['picture'] or None
    car_filter = CarFilter(request.GET, queryset=Car.objects.all())
    menu_brands = Brand.objects.all()
    menu_types = Category.objects.all()
    return {
        "user_base": user,
        "form_s": car_filter.form,
        "filtered_cars": car_filter.qs,
        "search": car_filter.form.cleaned_data.get('name', ''),
        "menu_brands": menu_brands,
        "menu_types": menu_types, 
        "profile_pic": profile_pic,
        "saved_cars": saved_cars,
        "customization": customization,
    }