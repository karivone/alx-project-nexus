from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended User model with additional fields"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_genres = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return self.email

# Create your models here.
