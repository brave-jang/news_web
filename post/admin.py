from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
    )


@admin.register(models.Category)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
