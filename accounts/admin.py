from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to be used in the admin interface.
    list_display = ('phone_number', 'is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('phone_number',)
    readonly_fields = ('last_login', 'date_joined')  # Ensure 'date_joined' is included if it's in your model

    # Define the fieldsets to be used in the admin.
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    ordering = ('phone_number',)

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
