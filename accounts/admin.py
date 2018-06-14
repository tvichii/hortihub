from django.contrib import admin
from .models import Profile, Contact
from django.contrib.auth.models import User

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

# class ContactInline(admin.TabularInline):
#     model = Contact
#     extra = 1
#
# class ContactAdmin(admin.ModelAdmin):
#     inlines = (ContactInline,)
#
# admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Contact, ContactAdmin)
