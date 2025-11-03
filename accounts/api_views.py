from django.contrib.auth import user_logged_in
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.user

                user_logged_in.send(sender=user.__class__, request=request, user=user)

            except Exception as e:
                pass
        return response


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer