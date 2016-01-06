import os


def facebook_app_id(request):
    context = {
        'facebook_app_id': os.getenv("FACEBOOK_APP_ID"),
    }
    return context
