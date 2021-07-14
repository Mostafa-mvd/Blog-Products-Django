from django.contrib import admin
from blog.models import Post, Category

# Register your models here.

# admin.site.register([Category, ])


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "creator", "image", "body", "like", "dislike")
    list_per_page = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_per_page = 4
