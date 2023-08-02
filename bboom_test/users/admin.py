from django.contrib import admin

from users.forms import CustomAuthenticationForm
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email"]
    list_display_links = ["id", "name"]
    fields = ["name", "email"]


admin.site.login_form = CustomAuthenticationForm
admin.site.login_template = 'admin/custom_login.html'
