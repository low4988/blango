from django.contrib import admin
# for translation in BlangoUserAdmin
from django.utils.translation import gettext_lazy as _

# To set up the admin is three steps. 
#Import models to register, then register
#1 Import UserAdmin:
from django.contrib.auth.admin import UserAdmin
#2 Import the User model:
from blango_auth.models import User

# Register your models here.
#3 Register the User model for the UserAdmin
# actual below class denfition, BlangoUserAdmin
# updated admin.site.register(User, UserAdmin) to
# for custom user 
#admin.site.register(User, BlangoUserAdmin)


# Build custom user UserAdmin
# override fieldsets, add_fieldsets, list_display, 
# search_fields and ordering attributes 
# replace username with email, and/or remove username, where appropriate.
# note the use of gettext_lazy as _ # imported above
class BlangoUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
#3
# updated admin.site.register(User, UserAdmin) to
# for custom user 
admin.site.register(User, BlangoUserAdmin)