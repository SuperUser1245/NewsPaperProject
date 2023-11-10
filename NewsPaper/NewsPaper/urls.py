from django.contrib import admin
from django.urls import path, include
from news.views import subscriptions

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('posts/', include('news.urls')),
    path('subscriptions/', subscriptions)
]
