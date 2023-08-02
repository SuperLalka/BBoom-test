from django.contrib import admin

from posts.models import Post


@admin.register(Post)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "body"]
