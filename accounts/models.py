from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None):
        
        if not username:
            raise ValueError('Please Enter a Username')
            
        user = self.model(
            username=username,
            )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, password):
        
        user = self.create_user(
            username,
            password=password,
            )
        
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user


class User(AbstractUser):
    
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    signed_in_once = models.BooleanField(default=False)
    saw_walkthrough = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
        
    latest_contact = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    
    objects = UserManager()
    
    class Meta:
        
        ordering = ('first_name', 'last_name')
        
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def as_dict(self):
        
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email
        }
        
        return data
    
    @property
    def full_name(self):
        
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        
        return 'N/A'
