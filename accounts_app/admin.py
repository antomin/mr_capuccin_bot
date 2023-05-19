from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts_app.forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'tgid', 'recv_reports']


admin.site.register(CustomUser, CustomUserAdmin)
