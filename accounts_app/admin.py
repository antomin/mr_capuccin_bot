from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from accounts_app.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username']


admin.site.register(CustomUser, CustomUserAdmin)
