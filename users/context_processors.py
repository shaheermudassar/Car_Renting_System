from users.models import Notification

def default(request):
    unseen = False  # Initialize variable to track unseen notifications
    if request.user.is_authenticated:  # Check if the user is authenticated
        if Notification.objects.filter(user=request.user, seen=False).exists():  # Check if there are any unseen notifications for the user
            unseen = True  # Set unseen to True if there are unseen notifications
    return {
        "unseen": unseen,  # Return the unseen variable in the context dictionary
    }
