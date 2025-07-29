from django.urls import path
from apps.users.views import RegisterView, LoginView, LogoutView, ActivateUserView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="user_registration"),
    path("login/", LoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate-user'),
]