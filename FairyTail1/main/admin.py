from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from main.models import CustomUser
from main.forms import RegisterForm, CustomUserChangeForm

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = RegisterForm
    form = CustomUserChangeForm

    list_display=['first_name', 'last_name', 'username', 'email', 'number', 'date_of_birth', 'country', 'city', ]

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields':(
                    'first_name',
                    'last_name',
                    'email',
                    'number',
                    'date_of_birth',
                    'country',
                    'city', 
                    'mailing'
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields':(
                    'number',
                    'date_of_birth',
                    'country',
                    'city', 
                    'mailing'
                )
            }
        )
    )