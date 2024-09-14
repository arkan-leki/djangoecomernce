from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        """
        Create and return a user with a phone number instead of a username.
        """
        if not phone:
            raise ValueError("The Phone number must be set")
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        Create and return a superuser with a phone number instead of a username.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone, password, **extra_fields)



class CustomUser(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']  # Email is required in addition to phone number

    def __str__(self):
        return self.phone
    
    
    def get_avatar(self):
        if self.profile_image:
            return self.profile_image.url
        return None  # or return a default image URL if needed
    
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this user.
        """
        if self.email:
            send_mail(subject, message, from_email, [self.email], **kwargs)
