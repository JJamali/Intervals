from django.contrib import admin
from intervalsApp.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'level', 'score')

admin.site.register(User, UserAdmin)