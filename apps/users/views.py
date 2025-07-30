from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import logout
from apps.users.models import AppUser
from apps.users.serializers import RegisterSerializer, LoginSerializer, UserLoginSerializer
from apps.users.messages import (
   REGISTRATION_SUCCESSFUL,
   REGISTRATION_FAILED,
   INVALID_CREDENTIALS,
   LOGIN_SUCCESSFUL,
   LOGIN_FAILED,
   INVALID_REFRESH_TOKEN,
   LOGOUT_SUCCESSFUL,
    ACTIVATION_FAILED,
)
from utils.mixins import ResponseViewMixin
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.utils import send_activation_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
class RegisterView(APIView, ResponseViewMixin):
    """
    Register View
    """

    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(user, request)
            return self.success_response(
                message=REGISTRATION_SUCCESSFUL
            )
        else:
            non_field_errors = serializer.errors.pop("non_field_errors", None)
            error_message = REGISTRATION_FAILED
            if non_field_errors:
                error_message = non_field_errors[0]
            return self.error_response(data=serializer.errors, message=error_message)

class LoginView(APIView, ResponseViewMixin):
    """
    Login View
    """
    permission_classes = []

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = AppUser.objects.filter(email=email).first()
            if user is None or not user.check_password(password):
                return self.error_response(
                    message=INVALID_CREDENTIALS,
                    data={},
                )
            if not user.is_active:
                return self.error_response(
                    message=ACTIVATION_FAILED,
                    data={}
                )
            if user is not None:
                RefreshToken.for_user(user)

            return self.success_response(
                data=UserLoginSerializer(user).data,
                message=LOGIN_SUCCESSFUL,
            )
        except Exception as e:
                return self.error_response(
                    message=LOGIN_FAILED, data=str(e))

class LogoutView(APIView, ResponseViewMixin):
    """
    Logout view
    """

    permission_classes = []

    def get(self, request):
        try:
            refresh = RefreshToken(request.data.get("refresh"))
            refresh.blacklist()
        except Exception as e:
            return self.error_response(
                message=INVALID_REFRESH_TOKEN, data=str(e)
            )

        logout(request)
        return self.success_response(message=LOGOUT_SUCCESSFUL)
    

class ActivateUserView(APIView, ResponseViewMixin):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AppUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return render(request, 'users/activation_success.html')
            else:
                return render(request, "users/activation_failed.html")
        except Exception as e:
            print(f"Activation error: {e}")
            return self.error_response(message="Activation failed.", data=str(e))



def register_page(request):
    """Render the registration form page"""
    return render(request, "users/register.html")


def login_page(request):
    """Render the login form page"""
    return render(request, "users/login.html")