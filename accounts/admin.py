from django.contrib import admin
from accounts.models import User


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    pass
