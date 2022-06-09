from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
# Register your models here.

class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff','is_user')


    fieldsets = (
        (None, {
            "fields": (
                
                'username',
                'email',
                'first_name',
                'last_name',
                'password',

            ), 
        }),
        ('Status', {
            "fields": (
                'is_active',
            ), 
        }),
        ("Permissions", {
            "fields": (
                'is_superuser',
                'is_admin',
                'is_staff',
                'is_user',

            ), 
        }),
        ("Special Permissions", {
            "fields": (
                'user_permissions',
            ), 
        }),
    )
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
