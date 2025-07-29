from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from apps.users.tasks import send_activation_email_task


def generate_activation_token(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_link = request.build_absolute_uri(
        reverse("activate-user", kwargs={"uidb64": uid, "token": token})
    )

    subject = "Activate Your Account"
    message = f"Hi {user.first_name},\n\nClick the link to activate your account:\n{activation_link}"
    send_activation_email_task.delay(subject, message, user.email)
