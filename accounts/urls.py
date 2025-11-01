from django.urls import path, include

from accounts.views import SignUpView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="sign-up"),
]

app_name = "accounts"
