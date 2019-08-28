import pdb
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    """Helps Django work with our custom user model"""

    def create_user(self, email, first_name, last_name, password=None):
        """"Create a new user profile object"""
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user  = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Creates and saves a new superuser with given details"""
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        user.is_admin     = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Represent a user profile inside our system. """

    email      = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    is_active  = models.BooleanField(default=True)
    is_admin   = models.BooleanField(default=False)

    objects   = UserManager()

    USERNAME_FIELD  = 'email'
    # REQUIRED_FIELDS = ()
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """Used to get a user's full name. """
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """Used to get a user's short name."""
        return self.first_name

    def __str__(self):
        """Django uses this when it needs to convert the object to a string"""
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return perm in self.get_all_permissions()

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
