from django.db import models

# Create your models here. blango_auth/models.py
# blog/settings.py, AUTH_USER_MODEL = "blango_auth.User" , INSTALLED_APPS+= "blango_auth"
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# for class User(AbstractUser): 
# email = models.EmailField(_("email address"), unique=True,)
# _ 
from django.utils.translation import gettext_lazy as _

# overrides _create_user(), create_user() and create_superuser()
# replacing the use of username with email
class BlangoUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

# User class should come after the BlangoUserManager class.
# Enable use of email as login  
# 
class User(AbstractUser):
    # The username field should be set to None.
    username = None

    # The email field should be the same on AbstractUser, except it should be unique and required.
    # applying a translation to the “email address” text, 
    # the same as the base class does, 
    # by wrapping it in the django.utils.translation.gettext_lazy function. 
    # django.utils.translation.gettext_lazy imported as _
    email = models.EmailField(_("email address"), unique=True,)

    # Set the objects attribute to an instance of BlangoUserManager
    objects = BlangoUserManager() # custom email-base class above

    # USERNAME_FIELD updated to new arbitrary field, 
    # matching User-attribute
    USERNAME_FIELD = "email"
    
    # REQUIRED_FIELDS = ["email"] as default
    # because by default this value is ["email"], 
    # however Django assumes the USERNAME_FIELD is required, 
    # and so doesn’t allow it to be listed in REQUIRED_FIELDS.

    # REQUIRED_FIELDS = [] empty as email is username, 
    #username is already assumed to always be required, 
    #therefore not entered here again
    REQUIRED_FIELDS = [] 

    def __str__(self):
        # return email instead of username
        return self.email    