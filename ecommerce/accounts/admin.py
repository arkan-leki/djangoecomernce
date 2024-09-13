from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser  # Import your CustomUser model

class CustomUserAdmin(BaseUserAdmin):
    # Fields to be used in displaying the User model
    list_display = ('phone', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Define the fieldsets for the admin layout
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'profile_image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to be used when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('phone', 'email', 'first_name', 'last_name')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register the CustomUser model and CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
