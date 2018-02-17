from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


class UserCreationForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return password2

    def save(self, commit=True):
        
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):

        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_admin', 'is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
    (None, {'fields': ('username', 'first_name', 'middle_name',
                       'last_name', 'password'
                       )}),
    ('Personal info', {'fields': ('email', 'role')}),
    ('Permissions', {'fields': ('is_admin','is_staff', 'is_active')}),
    )

    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('username', 'password1', 'password2')}
    ),
    )
    
search_fields = ('username',)
ordering = ('username',)
filter_horizontal = ()
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Team)
