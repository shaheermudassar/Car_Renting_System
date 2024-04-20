from users.models import Notification

def default(request):
    unseen = False
    if request.user.is_authenticated:
        if Notification.objects.filter(user = request.user, seen=False).exists():
            unseen = True
    return {
        "unseen": unseen,
    }