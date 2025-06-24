from django.contrib import admin
from user.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','role','photo']
    list_editable = ['photo']
