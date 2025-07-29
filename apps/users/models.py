from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.users.managers import CustomUserManager
from utils.models import TimeStampModel
import uuid

class AppUser(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """
    Custom User model where email is the unique identifier.
    Includes role-based access.
    """

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('agent', 'Agent'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='agent')
    is_admin = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


    @property
    def is_admin_user(self):
        return self.role == 'admin'

    @property
    def is_staff_user(self):
        return self.role == 'staff'

    @property
    def is_agent_user(self):
        return self.role == 'agent'
