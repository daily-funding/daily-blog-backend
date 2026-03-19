from django.conf import settings


def blog_settings(request):
    return {
        "BLOG_FRONTEND_URL": settings.BLOG_FRONTEND_URL,
    }
