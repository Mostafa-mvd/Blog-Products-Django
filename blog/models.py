from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name="category_name", max_length=100)
    slug = models.SlugField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = []
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Post(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created_time")
    title = models.CharField(verbose_name="title", max_length=100)
    category = models.ForeignKey("Category", verbose_name="category", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="my_post_image", upload_to="media/posts", blank=True, null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    like_btn_clicked = models.BooleanField(default=False)
    dislike_btn_clicked = models.BooleanField(default=False)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_unreal_like(self):
        key = f'unreal_like_key_{self.id}'
        val = cache.get(key, None)

        if val is None:
            unreal_like = self.like ** 2
            cache.set(key, unreal_like)
            return unreal_like
        return val
